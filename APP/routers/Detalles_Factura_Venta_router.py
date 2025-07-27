from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Detalles_Factura_Venta_schema import (
    DetalleFacturaVentaBase,
    DetalleFacturaVentaCreate,
    DetalleFacturaVentaUpdate,
    DetalleFacturaVentaSimple,
    DetalleFacturaVentaCompleta
)
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Productos_model import Productos
from ..DB.Inventario_model import Inventario
from ..DB.Usuarios_model import Usuarios
from ..DB.Movimientos_inventario_model import Movimientos_inventario
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/detalles-factura",
    tags=["Detalles de Factura"]
)

# Obtener detalles de una factura
@router.get("/factura/{factura_id}", response_model=List[DetalleFacturaVentaCompleta])
async def get_detalles_factura(
    factura_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar que la factura existe
    factura = db.query(Facturas_Venta).filter(Facturas_Venta.ID_Factura_Venta == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    detalles = db.query(
        Detalles_Factura_Venta,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU
    ).join(
        Productos,
        Detalles_Factura_Venta.ID_Producto == Productos.ID_Producto
    ).filter(
        Detalles_Factura_Venta.ID_Factura_Venta == factura_id
    ).all()
    
    return [
        {
            "id_detalle": d.Detalles_Factura_Venta.ID_Detalle,
            "producto": {
                "id": d.Detalles_Factura_Venta.ID_Producto,
                "nombre": d.nombre_producto,
                "codigo_barras": d.Codigo_Barras,
                "sku": d.SKU
            },
            "cantidad": d.Detalles_Factura_Venta.Cantidad,
            "precio_unitario": d.Detalles_Factura_Venta.Precio_Unitario,
            "descuento_unitario": d.Detalles_Factura_Venta.Descuento_Unitario,
            "subtotal": d.Detalles_Factura_Venta.Subtotal
        }
        for d in detalles
    ]

# Obtener un detalle específico
@router.get("/{detalle_id}", response_model=DetalleFacturaVentaCompleta)
async def get_detalle(
    detalle_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    detalle = db.query(Detalles_Factura_Venta).filter(
        Detalles_Factura_Venta.ID_Detalle == detalle_id
    ).first()
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    return detalle

# Actualizar detalle (solo si la factura está en estado pendiente)
@router.put("/{detalle_id}", response_model=DetalleFacturaVentaCompleta)
async def update_detalle(
    detalle: DetalleFacturaVentaUpdate,
    detalle_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_detalle = db.query(Detalles_Factura_Venta).filter(
        Detalles_Factura_Venta.ID_Detalle == detalle_id
    ).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    # Verificar estado de la factura
    factura = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Factura_Venta == db_detalle.ID_Factura_Venta
    ).first()
    if factura.Estado != "Pendiente":
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden modificar detalles de facturas pendientes"
        )
    
    # Si se modifica la cantidad, verificar stock
    if detalle.cantidad and detalle.cantidad != db_detalle.Cantidad:
        # Verificar stock disponible
        stock = db.query(Inventario).filter(
            Inventario.ID_Producto == db_detalle.ID_Producto,
            Inventario.ID_Sucursal == factura.ID_Sucursal
        ).first()
        
        diferencia = detalle.cantidad - db_detalle.Cantidad
        if stock.Stock_Actual < diferencia:
            raise HTTPException(
                status_code=400,
                detail="Stock insuficiente para la modificación"
            )
        
        # Actualizar stock
        stock.Stock_Actual -= diferencia
        stock.Fecha_Ultimo_Movimiento = datetime.now()
        
        # Registrar movimiento
        movimiento = Movimientos_inventario(
            ID_Producto=db_detalle.ID_Producto,
            ID_Sucursal=factura.ID_Sucursal,
            Tipo="Ajuste",
            Cantidad=-diferencia,
            ID_Usuario=current_user.ID_Usuario,
            ID_Referencia=factura.ID_Factura_Venta,
            Tipo_Referencia="Factura",
            Observaciones="Modificación de detalle de factura"
        )
        db.add(movimiento)
    
    # Actualizar campos
    if detalle.cantidad:
        db_detalle.Cantidad = detalle.cantidad
    if detalle.precio_unitario:
        db_detalle.Precio_Unitario = detalle.precio_unitario
    if detalle.descuento_unitario is not None:
        db_detalle.Descuento_Unitario = detalle.descuento_unitario
    
    # Recalcular subtotal
    db_detalle.Subtotal = (db_detalle.Cantidad * db_detalle.Precio_Unitario) - (db_detalle.Cantidad * db_detalle.Descuento_Unitario)
    
    # Recalcular totales de la factura
    detalles = db.query(Detalles_Factura_Venta).filter(
        Detalles_Factura_Venta.ID_Factura_Venta == factura.ID_Factura_Venta
    ).all()
    
    factura.Subtotal = sum(d.Subtotal for d in detalles)
    factura.Total = factura.Subtotal + factura.IVA - factura.Descuento
    
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

# Obtener estadísticas de productos vendidos
@router.get("/estadisticas/productos", response_model=List[dict])
async def get_estadisticas_productos(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    sucursal_id: Optional[int] = None,
    limite: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        Productos.Codigo_Barras,
        func.sum(Detalles_Factura_Venta.Cantidad).label('cantidad_vendida'),
        func.sum(Detalles_Factura_Venta.Subtotal).label('total_vendido'),
        func.count(Detalles_Factura_Venta.ID_Detalle).label('veces_vendido')
    ).join(
        Detalles_Factura_Venta
    ).join(
        Facturas_Venta,
        and_(
            Detalles_Factura_Venta.ID_Factura_Venta == Facturas_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != "Anulada"
        )
    )
    
    if desde:
        query = query.filter(Facturas_Venta.Fecha >= desde)
    if hasta:
        query = query.filter(Facturas_Venta.Fecha <= hasta)
    if sucursal_id:
        query = query.filter(Facturas_Venta.ID_Sucursal == sucursal_id)
    
    resultados = query.group_by(
        Productos.ID_Producto,
        Productos.Nombre,
        Productos.Codigo_Barras
    ).order_by(
        func.sum(Detalles_Factura_Venta.Cantidad).desc()
    ).limit(limite).all()
    
    return [
        {
            "producto": {
                "id": r.ID_Producto,
                "nombre": r.Nombre,
                "codigo_barras": r.Codigo_Barras
            },
            "cantidad_vendida": r.cantidad_vendida,
            "total_vendido": r.total_vendido,
            "veces_vendido": r.veces_vendido,
            "promedio_por_venta": round(r.cantidad_vendida / r.veces_vendido, 2)
        }
        for r in resultados
    ]

# Obtener historial de ventas de un producto
@router.get("/producto/{producto_id}/historial", response_model=List[dict])
async def get_historial_producto(
    producto_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar que el producto existe
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    query = db.query(
        Detalles_Factura_Venta,
        Facturas_Venta.Fecha,
        Facturas_Venta.Numero_Factura,
        Facturas_Venta.Estado
    ).join(
        Facturas_Venta
    ).filter(
        Detalles_Factura_Venta.ID_Producto == producto_id,
        Facturas_Venta.Estado != "Anulada"
    )
    
    if desde:
        query = query.filter(Facturas_Venta.Fecha >= desde)
    if hasta:
        query = query.filter(Facturas_Venta.Fecha <= hasta)
    
    ventas = query.order_by(Facturas_Venta.Fecha.desc()).all()
    
    return [
        {
            "fecha": v.Fecha,
            "factura": {
                "numero": v.Numero_Factura,
                "estado": v.Estado
            },
            "cantidad": v.Detalles_Factura_Venta.Cantidad,
            "precio_unitario": v.Detalles_Factura_Venta.Precio_Unitario,
            "descuento_unitario": v.Detalles_Factura_Venta.Descuento_Unitario,
            "subtotal": v.Detalles_Factura_Venta.Subtotal
        }
        for v in ventas
    ]
