from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Facturas_Venta_schema import (
    FacturaVentaBase,
    FacturaVentaCreate,
    FacturaVentaUpdate,
    FacturaVentaSimple,
    FacturaVentaCompleta,
    DetalleFacturaCreate
)
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Clientes_model import Clientes
from ..DB.Productos_model import Productos
from ..DB.Inventario_model import Inventario
from ..DB.Usuarios_model import Usuarios
from ..DB.Movimientos_inventario_model import Movimientos_inventario
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas de Venta"]
)

# Obtener todas las facturas con paginación y filtros
@router.get("/", response_model=List[FacturaVentaSimple])
async def get_facturas(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    cliente_id: Optional[int] = Query(None, description="Filtrar por cliente"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    tipo_factura: Optional[str] = Query(None, description="Tipo de factura (A, B, C)"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(Facturas_Venta)
    
    # Aplicar filtros
    if cliente_id:
        query = query.filter(Facturas_Venta.ID_Cliente == cliente_id)
    if sucursal_id:
        query = query.filter(Facturas_Venta.ID_Sucursal == sucursal_id)
    if estado:
        query = query.filter(Facturas_Venta.Estado == estado)
    if desde:
        query = query.filter(Facturas_Venta.Fecha >= desde)
    if hasta:
        query = query.filter(Facturas_Venta.Fecha <= hasta)
    if tipo_factura:
        query = query.filter(Facturas_Venta.Tipo_Factura == tipo_factura)
    
    total = query.count()
    facturas = query.order_by(Facturas_Venta.Fecha.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": facturas,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una factura por ID
@router.get("/{factura_id}", response_model=FacturaVentaCompleta)
async def get_factura(
    factura_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    factura = db.query(Facturas_Venta).filter(Facturas_Venta.ID_Factura_Venta == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

# Crear nueva factura
@router.post("/", response_model=FacturaVentaCompleta)
async def create_factura(
    factura: FacturaVentaCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar cliente
    cliente = db.query(Clientes).filter(
        Clientes.ID_Cliente == factura.id_cliente,
        Clientes.Activo == True
    ).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado o inactivo")
    
    # Verificar límite de crédito si la factura no es de contado
    if factura.forma_pago != "Contado":
        saldo_pendiente = cliente.Saldo_Actual + factura.total
        if saldo_pendiente > cliente.Limite_Credito:
            raise HTTPException(
                status_code=400,
                detail="El cliente excedería su límite de crédito"
            )
    
    # Verificar productos y stock
    for detalle in factura.detalles:
        # Verificar producto
        producto = db.query(Productos).filter(
            Productos.ID_Producto == detalle.id_producto,
            Productos.Activo == True
        ).first()
        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto {detalle.id_producto} no encontrado o inactivo"
            )
        
        # Verificar stock
        stock = db.query(Inventario).filter(
            Inventario.ID_Producto == detalle.id_producto,
            Inventario.ID_Sucursal == factura.id_sucursal
        ).first()
        if not stock or stock.Stock_Actual < detalle.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para el producto {producto.Nombre}"
            )
        
        # Verificar precio
        if detalle.precio_unitario < producto.Costo:
            raise HTTPException(
                status_code=400,
                detail=f"Precio inválido para el producto {producto.Nombre}"
            )
    
    # Crear factura
    db_factura = Facturas_Venta(
        ID_Cliente=factura.id_cliente,
        ID_Sucursal=factura.id_sucursal,
        Tipo_Factura=factura.tipo_factura,
        Condicion_IVA=cliente.Condicion_IVA,
        Subtotal=factura.subtotal,
        IVA=factura.iva,
        Descuento=factura.descuento,
        Total=factura.total,
        ID_Usuario=current_user.ID_Usuario,
        Estado="Emitida",
        Forma_Pago=factura.forma_pago,
        Observaciones=factura.observaciones
    )
    db.add(db_factura)
    db.flush()  # Para obtener el ID de la factura
    
    # Crear detalles y actualizar stock
    for detalle in factura.detalles:
        db_detalle = Detalles_Factura_Venta(
            ID_Factura_Venta=db_factura.ID_Factura_Venta,
            ID_Producto=detalle.id_producto,
            Cantidad=detalle.cantidad,
            Precio_Unitario=detalle.precio_unitario,
            Descuento_Unitario=detalle.descuento_unitario,
            Subtotal=detalle.subtotal
        )
        db.add(db_detalle)
        
        # Actualizar stock
        stock = db.query(Inventario).filter(
            Inventario.ID_Producto == detalle.id_producto,
            Inventario.ID_Sucursal == factura.id_sucursal
        ).first()
        stock.Stock_Actual -= detalle.cantidad
        stock.Fecha_Ultimo_Movimiento = datetime.now()
        
        # Registrar movimiento
        movimiento = Movimientos_inventario(
            ID_Producto=detalle.id_producto,
            ID_Sucursal=factura.id_sucursal,
            Tipo="Venta",
            Cantidad=-detalle.cantidad,
            ID_Usuario=current_user.ID_Usuario,
            ID_Referencia=db_factura.ID_Factura_Venta,
            Tipo_Referencia="Factura"
        )
        db.add(movimiento)
    
    # Actualizar saldo del cliente si no es de contado
    if factura.forma_pago != "Contado":
        cliente.Saldo_Actual += factura.total
    
    db.commit()
    db.refresh(db_factura)
    return db_factura

# Anular factura
@router.post("/{factura_id}/anular")
async def anular_factura(
    factura_id: int = Path(..., gt=0),
    motivo: str = Query(..., min_length=5, max_length=200),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    factura = db.query(Facturas_Venta).filter(Facturas_Venta.ID_Factura_Venta == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    if factura.Estado == "Anulada":
        raise HTTPException(status_code=400, detail="La factura ya está anulada")
    
    # Restaurar stock
    detalles = db.query(Detalles_Factura_Venta).filter(
        Detalles_Factura_Venta.ID_Factura_Venta == factura_id
    ).all()
    
    for detalle in detalles:
        stock = db.query(Inventario).filter(
            Inventario.ID_Producto == detalle.ID_Producto,
            Inventario.ID_Sucursal == factura.ID_Sucursal
        ).first()
        stock.Stock_Actual += detalle.Cantidad
        stock.Fecha_Ultimo_Movimiento = datetime.now()
        
        # Registrar movimiento
        movimiento = Movimientos_inventario(
            ID_Producto=detalle.ID_Producto,
            ID_Sucursal=factura.ID_Sucursal,
            Tipo="Anulación",
            Cantidad=detalle.Cantidad,
            ID_Usuario=current_user.ID_Usuario,
            ID_Referencia=factura_id,
            Tipo_Referencia="Factura",
            Observaciones=f"Anulación de factura: {motivo}"
        )
        db.add(movimiento)
    
    # Restaurar saldo del cliente si no era de contado
    if factura.Forma_Pago != "Contado":
        cliente = db.query(Clientes).filter(Clientes.ID_Cliente == factura.ID_Cliente).first()
        cliente.Saldo_Actual -= factura.Total
    
    factura.Estado = "Anulada"
    db.commit()
    
    return {"message": "Factura anulada correctamente"}

# Obtener estadísticas de ventas
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_ventas(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(Facturas_Venta).filter(Facturas_Venta.Estado != "Anulada")
    
    if desde:
        query = query.filter(Facturas_Venta.Fecha >= desde)
    if hasta:
        query = query.filter(Facturas_Venta.Fecha <= hasta)
    if sucursal_id:
        query = query.filter(Facturas_Venta.ID_Sucursal == sucursal_id)
    
    # Totales
    totales = query.with_entities(
        func.count(Facturas_Venta.ID_Factura_Venta).label('cantidad_facturas'),
        func.sum(Facturas_Venta.Total).label('total_ventas'),
        func.avg(Facturas_Venta.Total).label('promedio_venta')
    ).first()
    
    # Ventas por tipo de factura
    por_tipo = db.query(
        Facturas_Venta.Tipo_Factura,
        func.count(Facturas_Venta.ID_Factura_Venta).label('cantidad'),
        func.sum(Facturas_Venta.Total).label('total')
    ).filter(
        Facturas_Venta.Estado != "Anulada"
    ).group_by(Facturas_Venta.Tipo_Factura).all()
    
    # Ventas por forma de pago
    por_forma_pago = db.query(
        Facturas_Venta.Forma_Pago,
        func.count(Facturas_Venta.ID_Factura_Venta).label('cantidad'),
        func.sum(Facturas_Venta.Total).label('total')
    ).filter(
        Facturas_Venta.Estado != "Anulada"
    ).group_by(Facturas_Venta.Forma_Pago).all()
    
    return {
        "totales": {
            "cantidad_facturas": totales.cantidad_facturas or 0,
            "total_ventas": totales.total_ventas or 0,
            "promedio_venta": round(totales.promedio_venta or 0, 2)
        },
        "por_tipo_factura": [
            {
                "tipo": t.Tipo_Factura,
                "cantidad": t.cantidad,
                "total": t.total
            }
            for t in por_tipo
        ],
        "por_forma_pago": [
            {
                "forma_pago": f.Forma_Pago,
                "cantidad": f.cantidad,
                "total": f.total
            }
            for f in por_forma_pago
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
