from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Productos_Descuentos_schema import (
    ProductoDescuentoBase,
    ProductoDescuentoCreate,
    ProductoDescuentoUpdate,
    ProductoDescuentoSimple,
    ProductoDescuentoCompleto,
    ResumenDescuentosProducto,
    AnalisisEfectividadDescuentos
)
from ..DB.Productos_Descuentos_model import Productos_Descuentos
from ..DB.Productos_model import Productos
from ..DB.Descuentos_model import Descuentos
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case, distinct, or_
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/productos-descuentos",
    tags=["Productos con Descuentos"]
)

# Obtener descuentos por producto
@router.get("/producto/{producto_id}", response_model=List[ProductoDescuentoCompleto])
async def get_descuentos_producto(
    producto_id: int = Path(..., gt=0),
    activos: Optional[bool] = Query(None, description="Filtrar por descuentos activos"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar que el producto existe
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    query = db.query(
        Productos_Descuentos,
        Descuentos
    ).join(
        Descuentos
    ).filter(
        Productos_Descuentos.ID_Producto == producto_id
    )
    
    if activos is not None:
        hoy = datetime.now().date()
        if activos:
            query = query.filter(
                Descuentos.Fecha_Inicio <= hoy,
                Descuentos.Fecha_Fin >= hoy,
                Descuentos.Activo == True
            )
        else:
            query = query.filter(
                or_(
                    Descuentos.Fecha_Fin < hoy,
                    Descuentos.Activo == False
                )
            )
    
    descuentos = query.all()
    
    resultados = []
    for d in descuentos:
        precio_con_descuento = producto.Precio
        if d.Descuentos.Tipo_Descuento == "Porcentaje":
            precio_con_descuento *= (1 - d.Descuentos.Porcentaje/100)
        else:
            precio_con_descuento -= d.Descuentos.Monto_Fijo
        
        resultados.append({
            "producto": {
                "id": producto.ID_Producto,
                "nombre": producto.Nombre,
                "precio_original": producto.Precio
            },
            "descuento": {
                "id": d.Descuentos.ID_Descuento,
                "nombre": d.Descuentos.Nombre,
                "tipo": d.Descuentos.Tipo_Descuento,
                "valor": d.Descuentos.Porcentaje or d.Descuentos.Monto_Fijo,
                "fecha_inicio": d.Descuentos.Fecha_Inicio,
                "fecha_fin": d.Descuentos.Fecha_Fin,
                "activo": d.Descuentos.Activo
            },
            "precio_con_descuento": precio_con_descuento,
            "ahorro": producto.Precio - precio_con_descuento,
            "porcentaje_ahorro": round((producto.Precio - precio_con_descuento) / producto.Precio * 100, 2)
        })
    
    return resultados

# Obtener productos por descuento
@router.get("/descuento/{descuento_id}", response_model=List[ProductoDescuentoCompleto])
async def get_productos_descuento(
    descuento_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar que el descuento existe
    descuento = db.query(Descuentos).filter(Descuentos.ID_Descuento == descuento_id).first()
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    
    productos = db.query(
        Productos_Descuentos,
        Productos
    ).join(
        Productos
    ).filter(
        Productos_Descuentos.ID_Descuento == descuento_id,
        Productos.Activo == True
    ).all()
    
    resultados = []
    for p in productos:
        precio_con_descuento = p.Productos.Precio
        if descuento.Tipo_Descuento == "Porcentaje":
            precio_con_descuento *= (1 - descuento.Porcentaje/100)
        else:
            precio_con_descuento -= descuento.Monto_Fijo
        
        # Obtener ventas con este descuento
        ventas = db.query(
            func.count(Detalles_Factura_Venta.ID_Detalle).label('cantidad_ventas'),
            func.sum(Detalles_Factura_Venta.Cantidad).label('unidades_vendidas'),
            func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
        ).join(
            Facturas_Venta,
            and_(
                Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
                Facturas_Venta.Estado != 'Anulada',
                Facturas_Venta.Fecha.between(descuento.Fecha_Inicio, descuento.Fecha_Fin)
            )
        ).filter(
            Detalles_Factura_Venta.ID_Producto == p.Productos.ID_Producto
        ).first()
        
        resultados.append({
            "producto": {
                "id": p.Productos.ID_Producto,
                "nombre": p.Productos.Nombre,
                "codigo_barras": p.Productos.Codigo_Barras,
                "precio_original": p.Productos.Precio
            },
            "descuento": {
                "id": descuento.ID_Descuento,
                "nombre": descuento.Nombre,
                "tipo": descuento.Tipo_Descuento,
                "valor": descuento.Porcentaje or descuento.Monto_Fijo
            },
            "precio_con_descuento": precio_con_descuento,
            "ahorro": p.Productos.Precio - precio_con_descuento,
            "estadisticas": {
                "ventas": ventas.cantidad_ventas or 0,
                "unidades": ventas.unidades_vendidas or 0,
                "total_descuento": ventas.total_descuento or 0
            }
        })
    
    return resultados

# Análisis de efectividad de descuentos
@router.get("/analisis", response_model=AnalisisEfectividadDescuentos)
async def get_analisis_efectividad(
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
    
    # Análisis por tipo de descuento
    por_tipo = db.query(
        Descuentos.Tipo_Descuento,
        func.count(distinct(Productos_Descuentos.ID_Producto)).label('productos'),
        func.count(distinct(Detalles_Factura_Venta.ID_Factura_Venta)).label('ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('unidades'),
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
    ).join(
        Productos_Descuentos,
        Productos_Descuentos.ID_Descuento == Descuentos.ID_Descuento
    ).join(
        Detalles_Factura_Venta,
        Detalles_Factura_Venta.ID_Producto == Productos_Descuentos.ID_Producto
    ).join(
        Facturas_Venta,
        and_(
            Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada',
            Facturas_Venta.Fecha.between(desde, hasta)
        )
    ).group_by(
        Descuentos.Tipo_Descuento
    ).all()
    
    # Productos más efectivos con descuentos
    productos_efectivos = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        func.count(distinct(Descuentos.ID_Descuento)).label('descuentos_aplicados'),
        func.count(distinct(Detalles_Factura_Venta.ID_Factura_Venta)).label('ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('unidades'),
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
    ).join(
        Productos_Descuentos,
        Productos_Descuentos.ID_Producto == Productos.ID_Producto
    ).join(
        Descuentos,
        Descuentos.ID_Descuento == Productos_Descuentos.ID_Descuento
    ).join(
        Detalles_Factura_Venta,
        Detalles_Factura_Venta.ID_Producto == Productos.ID_Producto
    ).join(
        Facturas_Venta,
        and_(
            Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada',
            Facturas_Venta.Fecha.between(desde, hasta)
        )
    ).group_by(
        Productos.ID_Producto,
        Productos.Nombre
    ).order_by(
        func.sum(Detalles_Factura_Venta.Cantidad).desc()
    ).limit(10).all()
    
    return {
        "por_tipo": [
            {
                "tipo": t.Tipo_Descuento,
                "productos": t.productos,
                "ventas": t.ventas,
                "unidades": t.unidades,
                "total_descuento": t.total_descuento,
                "promedio_por_venta": round(t.total_descuento / t.ventas if t.ventas > 0 else 0, 2)
            }
            for t in por_tipo
        ],
        "productos_efectivos": [
            {
                "producto": {
                    "id": p.ID_Producto,
                    "nombre": p.Nombre
                },
                "descuentos_aplicados": p.descuentos_aplicados,
                "ventas": p.ventas,
                "unidades": p.unidades,
                "total_descuento": p.total_descuento,
                "promedio_por_unidad": round(p.total_descuento / p.unidades if p.unidades > 0 else 0, 2)
            }
            for p in productos_efectivos
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
