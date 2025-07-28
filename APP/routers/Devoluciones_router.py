from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Devoluciones_schema import (
    DevolucionBase,
    DevolucionCreate,
    DevolucionUpdate,
    DevolucionSimple,
    DevolucionCompleta,
    DetalleDevolucionCreate,
    EstadisticasDevoluciones
)
from ..DB.Devoluciones_model import Devoluciones
from ..DB.Detalles_Devolucion_model import Detalles_Devolucion
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Productos_model import Productos
from ..DB.Inventario_model import Inventario
from ..DB.Movimientos_inventario_model import Movimientos_inventario
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case, distinct
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/devoluciones",
    tags=["Devoluciones"]
)

# Obtener todas las devoluciones con filtros
@router.get("/", response_model=List[DevolucionSimple])
async def get_devoluciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    factura_id: Optional[int] = Query(None, description="Filtrar por factura"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Devoluciones,
        Facturas_Venta.Numero_Factura,
        func.count(Detalles_Devolucion.ID_Detalle_Devolucion).label('cantidad_items'),
        func.sum(Detalles_Devolucion.Cantidad).label('total_unidades')
    ).join(
        Facturas_Venta
    ).join(
        Detalles_Devolucion
    ).group_by(
        Devoluciones.ID_Devolucion,
        Facturas_Venta.Numero_Factura
    )
    
    # Aplicar filtros
    if estado:
        query = query.filter(Devoluciones.Estado == estado)
    if factura_id:
        query = query.filter(Devoluciones.ID_Factura_Venta == factura_id)
    if desde:
        query = query.filter(Devoluciones.Fecha_Devolucion >= desde)
    if hasta:
        query = query.filter(Devoluciones.Fecha_Devolucion <= hasta)
    
    total = query.count()
    devoluciones = query.order_by(Devoluciones.Fecha_Devolucion.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_devolucion": d.Devoluciones.ID_Devolucion,
                "factura": {
                    "id": d.Devoluciones.ID_Factura_Venta,
                    "numero": d.Numero_Factura
                },
                "fecha": d.Devoluciones.Fecha_Devolucion,
                "estado": d.Devoluciones.Estado,
                "motivo": d.Devoluciones.Motivo,
                "items": d.cantidad_items,
                "unidades": d.total_unidades
            }
            for d in devoluciones
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una devolución específica
@router.get("/{devolucion_id}", response_model=DevolucionCompleta)
async def get_devolucion(
    devolucion_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    devolucion = db.query(
        Devoluciones,
        Facturas_Venta.Numero_Factura,
        Facturas_Venta.Fecha.label('fecha_factura')
    ).join(
        Facturas_Venta
    ).filter(
        Devoluciones.ID_Devolucion == devolucion_id
    ).first()
    
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    
    # Obtener detalles
    detalles = db.query(
        Detalles_Devolucion,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Detalles_Factura_Venta.Precio_Unitario
    ).join(
        Productos
    ).join(
        Detalles_Factura_Venta,
        and_(
            Detalles_Factura_Venta.ID_Factura_Venta == devolucion.Devoluciones.ID_Factura_Venta,
            Detalles_Factura_Venta.ID_Producto == Detalles_Devolucion.ID_Producto
        )
    ).filter(
        Detalles_Devolucion.ID_Devolucion == devolucion_id
    ).all()
    
    return {
        "devolucion": {
            "id_devolucion": devolucion.Devoluciones.ID_Devolucion,
            "factura": {
                "id": devolucion.Devoluciones.ID_Factura_Venta,
                "numero": devolucion.Numero_Factura,
                "fecha": devolucion.fecha_factura
            },
            "fecha_devolucion": devolucion.Devoluciones.Fecha_Devolucion,
            "estado": devolucion.Devoluciones.Estado,
            "motivo": devolucion.Devoluciones.Motivo,
            "observaciones": devolucion.Devoluciones.Observaciones
        },
        "detalles": [
            {
                "producto": {
                    "id": d.Detalles_Devolucion.ID_Producto,
                    "nombre": d.nombre_producto,
                    "codigo_barras": d.Codigo_Barras
                },
                "cantidad": d.Detalles_Devolucion.Cantidad,
                "precio_unitario": d.Precio_Unitario,
                "subtotal": d.Precio_Unitario * d.Detalles_Devolucion.Cantidad,
                "motivo_especifico": d.Detalles_Devolucion.Motivo_Especifico
            }
            for d in detalles
        ],
        "totales": {
            "items": len(detalles),
            "unidades": sum(d.Detalles_Devolucion.Cantidad for d in detalles),
            "monto": sum(d.Precio_Unitario * d.Detalles_Devolucion.Cantidad for d in detalles)
        }
    }

# Crear nueva devolución
@router.post("/", response_model=DevolucionCompleta)
async def create_devolucion(
    devolucion: DevolucionCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar factura
    factura = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Factura_Venta == devolucion.id_factura_venta
    ).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    if factura.Estado == "Anulada":
        raise HTTPException(status_code=400, detail="No se pueden procesar devoluciones de facturas anuladas")
    
    # Verificar productos y cantidades
    detalles_factura = {
        d.ID_Producto: d.Cantidad for d in db.query(Detalles_Factura_Venta).filter(
            Detalles_Factura_Venta.ID_Factura_Venta == devolucion.id_factura_venta
        ).all()
    }
    
    # Verificar devoluciones previas
    devoluciones_previas = {
        d.ID_Producto: func.sum(d.Cantidad) for d in db.query(Detalles_Devolucion).join(
            Devoluciones,
            and_(
                Devoluciones.ID_Devolucion == Detalles_Devolucion.ID_Devolucion,
                Devoluciones.ID_Factura_Venta == devolucion.id_factura_venta,
                Devoluciones.Estado != 'Rechazada'
            )
        ).group_by(Detalles_Devolucion.ID_Producto).all()
    }
    
    for detalle in devolucion.detalles:
        if detalle.id_producto not in detalles_factura:
            raise HTTPException(
                status_code=400,
                detail=f"El producto {detalle.id_producto} no está en la factura"
            )
        
        cantidad_disponible = detalles_factura[detalle.id_producto] - (
            devoluciones_previas.get(detalle.id_producto, 0)
        )
        
        if detalle.cantidad > cantidad_disponible:
            raise HTTPException(
                status_code=400,
                detail=f"La cantidad a devolver del producto {detalle.id_producto} excede lo disponible"
            )
    
    # Crear devolución
    db_devolucion = Devoluciones(
        ID_Factura_Venta=devolucion.id_factura_venta,
        Motivo=devolucion.motivo,
        Estado="Pendiente",
        ID_Usuario=current_user.ID_Usuario,
        Observaciones=devolucion.observaciones
    )
    db.add(db_devolucion)
    db.flush()
    
    # Crear detalles
    for detalle in devolucion.detalles:
        db_detalle = Detalles_Devolucion(
            ID_Devolucion=db_devolucion.ID_Devolucion,
            ID_Producto=detalle.id_producto,
            Cantidad=detalle.cantidad,
            Motivo_Especifico=detalle.motivo_especifico
        )
        db.add(db_detalle)
    
    db.commit()
    db.refresh(db_devolucion)
    
    return await get_devolucion(db_devolucion.ID_Devolucion, db, current_user)

# Actualizar estado de devolución
@router.patch("/{devolucion_id}/estado")
async def update_estado_devolucion(
    devolucion_id: int = Path(..., gt=0),
    estado: str = Query(..., description="Nuevo estado de la devolución"),
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    devolucion = db.query(Devoluciones).filter(Devoluciones.ID_Devolucion == devolucion_id).first()
    if not devolucion:
        raise HTTPException(status_code=404, detail="Devolución no encontrada")
    
    estados_validos = {
        "Pendiente": ["Aprobada", "Rechazada"],
        "Aprobada": ["Completada"],
        "Rechazada": [],
        "Completada": []
    }
    
    if estado not in estados_validos.get(devolucion.Estado, []):
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar el estado de {devolucion.Estado} a {estado}"
        )
    
    # Si se aprueba, verificar stock
    if estado == "Aprobada":
        detalles = db.query(Detalles_Devolucion).filter(
            Detalles_Devolucion.ID_Devolucion == devolucion_id
        ).all()
        
        factura = db.query(Facturas_Venta).filter(
            Facturas_Venta.ID_Factura_Venta == devolucion.ID_Factura_Venta
        ).first()
        
        for detalle in detalles:
            # Actualizar o crear registro de inventario
            inventario = db.query(Inventario).filter(
                Inventario.ID_Producto == detalle.ID_Producto,
                Inventario.ID_Sucursal == factura.ID_Sucursal
            ).first()
            
            if not inventario:
                inventario = Inventario(
                    ID_Producto=detalle.ID_Producto,
                    ID_Sucursal=factura.ID_Sucursal,
                    Stock_Actual=0,
                    Stock_Minimo=0,
                    Stock_Maximo=999999
                )
                db.add(inventario)
                db.flush()
            
            # Actualizar stock
            inventario.Stock_Actual += detalle.Cantidad
            inventario.Fecha_Ultimo_Movimiento = datetime.now()
            
            # Registrar movimiento
            movimiento = Movimientos_inventario(
                ID_Producto=detalle.ID_Producto,
                ID_Sucursal=factura.ID_Sucursal,
                Tipo="Devolucion",
                Cantidad=detalle.Cantidad,
                ID_Usuario=current_user.ID_Usuario,
                ID_Referencia=devolucion_id,
                Tipo_Referencia="Devolucion",
                Observaciones=f"Devolución de factura {factura.Numero_Factura}"
            )
            db.add(movimiento)
    
    # Actualizar estado
    devolucion.Estado = estado
    if observaciones:
        devolucion.Observaciones = (devolucion.Observaciones or "") + f"\n[{datetime.now()}] {estado}: {observaciones}"
    
    db.commit()
    
    return {"message": f"Estado actualizado a {estado}"}

# Obtener estadísticas de devoluciones
@router.get("/estadisticas", response_model=EstadisticasDevoluciones)
async def get_estadisticas_devoluciones(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    if not desde:
        desde = datetime.now() - timedelta(days=30)
    if not hasta:
        hasta = datetime.now()
    
    # Devoluciones por estado
    por_estado = db.query(
        Devoluciones.Estado,
        func.count(Devoluciones.ID_Devolucion).label('total'),
        func.count(distinct(Detalles_Devolucion.ID_Producto)).label('productos_distintos'),
        func.sum(Detalles_Devolucion.Cantidad).label('unidades')
    ).join(
        Detalles_Devolucion
    ).filter(
        Devoluciones.Fecha_Devolucion.between(desde, hasta)
    ).group_by(
        Devoluciones.Estado
    ).all()
    
    # Productos más devueltos
    productos_devueltos = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        func.count(Devoluciones.ID_Devolucion).label('devoluciones'),
        func.sum(Detalles_Devolucion.Cantidad).label('unidades')
    ).join(
        Detalles_Devolucion,
        Detalles_Devolucion.ID_Producto == Productos.ID_Producto
    ).join(
        Devoluciones,
        and_(
            Devoluciones.ID_Devolucion == Detalles_Devolucion.ID_Devolucion,
            Devoluciones.Estado != 'Rechazada',
            Devoluciones.Fecha_Devolucion.between(desde, hasta)
        )
    ).group_by(
        Productos.ID_Producto,
        Productos.Nombre
    ).order_by(
        func.sum(Detalles_Devolucion.Cantidad).desc()
    ).limit(10).all()
    
    return {
        "por_estado": [
            {
                "estado": e.Estado,
                "total": e.total,
                "productos_distintos": e.productos_distintos,
                "unidades": e.unidades
            }
            for e in por_estado
        ],
        "productos_mas_devueltos": [
            {
                "producto": {
                    "id": p.ID_Producto,
                    "nombre": p.Nombre
                },
                "devoluciones": p.devoluciones,
                "unidades": p.unidades
            }
            for p in productos_devueltos
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
