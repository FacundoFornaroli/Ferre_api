from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Detalle_OC_schema import (
    DetalleOCBase,
    DetalleOCCreate,
    DetalleOCUpdate,
    DetalleOCSimple,
    DetalleOCCompleto,
    AnalisisCostos
)
from APP.DB.Detalle_OC_model import Detalle_OC
from APP.DB.Ordenes_Compra_model import Ordenes_Compra
from APP.DB.Productos_model import Productos
from APP.DB.Inventario_model import Inventario
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/detalle-oc",
    tags=["Detalles de Orden de Compra"]
)

# Obtener detalles de una orden de compra
@router.get("/orden/{orden_id}", response_model=List[DetalleOCCompleto])
async def get_detalles_orden(
    orden_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar que la orden existe
    orden = db.query(Ordenes_Compra).filter(Ordenes_Compra.ID_OC == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    detalles = db.query(
        Detalle_OC,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU,
        Productos.Marca
    ).join(
        Productos
    ).filter(
        Detalle_OC.ID_OC == orden_id
    ).all()
    
    # Obtener costos anteriores para comparación
    resultados = []
    for detalle in detalles:
        # Buscar último costo registrado antes de esta orden
        costo_anterior = db.query(Detalle_OC.Costo_Unitario).join(
            Ordenes_Compra
        ).filter(
            Detalle_OC.ID_Producto == detalle.Detalle_OC.ID_Producto,
            Ordenes_Compra.Fecha < orden.Fecha,
            Ordenes_Compra.Estado == 'Recibida'
        ).order_by(
            Ordenes_Compra.Fecha.desc()
        ).first()
        
        # Calcular variación de costo
        costo_anterior = costo_anterior[0] if costo_anterior else detalle.Detalle_OC.Costo_Unitario
        variacion = ((detalle.Detalle_OC.Costo_Unitario - costo_anterior) / costo_anterior * 100) if costo_anterior > 0 else 0
        
        # Obtener stock actual
        stock = db.query(func.sum(Inventario.Stock_Actual)).filter(
            Inventario.ID_Producto == detalle.Detalle_OC.ID_Producto
        ).scalar() or 0
        
        resultados.append({
            "detalle": {
                "id_detalle": detalle.Detalle_OC.ID_Detalle_OC,
                "producto": {
                    "id": detalle.Detalle_OC.ID_Producto,
                    "nombre": detalle.nombre_producto,
                    "codigo_barras": detalle.Codigo_Barras,
                    "sku": detalle.SKU,
                    "marca": detalle.Marca
                },
                "cantidad": detalle.Detalle_OC.Cantidad,
                "costo_unitario": detalle.Detalle_OC.Costo_Unitario,
                "descuento_unitario": detalle.Detalle_OC.Descuento_Unitario,
                "subtotal": detalle.Detalle_OC.Subtotal
            },
            "analisis": {
                "costo_anterior": costo_anterior,
                "variacion_porcentual": round(variacion, 2),
                "stock_actual": stock,
                "costo_promedio": (costo_anterior + detalle.Detalle_OC.Costo_Unitario) / 2
            }
        })
    
    return resultados

# Obtener un detalle específico
@router.get("/{detalle_id}", response_model=DetalleOCCompleto)
async def get_detalle(
    detalle_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    detalle = db.query(
        Detalle_OC,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU,
        Productos.Marca,
        Ordenes_Compra.Fecha.label('fecha_orden'),
        Ordenes_Compra.Estado.label('estado_orden')
    ).join(
        Productos
    ).join(
        Ordenes_Compra
    ).filter(
        Detalle_OC.ID_Detalle_OC == detalle_id
    ).first()
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    return {
        "detalle": {
            "id_detalle": detalle.Detalle_OC.ID_Detalle_OC,
            "orden": {
                "id": detalle.Detalle_OC.ID_OC,
                "fecha": detalle.fecha_orden,
                "estado": detalle.estado_orden
            },
            "producto": {
                "id": detalle.Detalle_OC.ID_Producto,
                "nombre": detalle.nombre_producto,
                "codigo_barras": detalle.Codigo_Barras,
                "sku": detalle.SKU,
                "marca": detalle.Marca
            },
            "cantidad": detalle.Detalle_OC.Cantidad,
            "costo_unitario": detalle.Detalle_OC.Costo_Unitario,
            "descuento_unitario": detalle.Detalle_OC.Descuento_Unitario,
            "subtotal": detalle.Detalle_OC.Subtotal
        }
    }

# Actualizar detalle (solo si la orden está pendiente)
@router.put("/{detalle_id}", response_model=DetalleOCCompleto)
async def update_detalle(
    detalle: DetalleOCUpdate,
    detalle_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_detalle = db.query(Detalle_OC).filter(Detalle_OC.ID_Detalle_OC == detalle_id).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    # Verificar estado de la orden
    orden = db.query(Ordenes_Compra).filter(
        Ordenes_Compra.ID_OC == db_detalle.ID_OC
    ).first()
    
    if orden.Estado != "Pendiente":
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden modificar detalles de órdenes pendientes"
        )
    
    # Actualizar campos
    if detalle.cantidad:
        db_detalle.Cantidad = detalle.cantidad
    if detalle.costo_unitario:
        db_detalle.Costo_Unitario = detalle.costo_unitario
    if detalle.descuento_unitario is not None:
        db_detalle.Descuento_Unitario = detalle.descuento_unitario
    
    # Recalcular subtotal
    db_detalle.Subtotal = (db_detalle.Cantidad * db_detalle.Costo_Unitario) - (db_detalle.Cantidad * db_detalle.Descuento_Unitario)
    
    # Recalcular totales de la orden
    detalles = db.query(Detalle_OC).filter(
        Detalle_OC.ID_OC == orden.ID_OC
    ).all()
    
    orden.Subtotal = sum(d.Subtotal for d in detalles)
    orden.IVA = orden.Subtotal * 0.21  # 21% de IVA
    orden.Total = orden.Subtotal + orden.IVA - orden.Descuento
    
    db.commit()
    db.refresh(db_detalle)
    
    return await get_detalle(detalle_id, db, current_user)

# Análisis de costos por producto
@router.get("/producto/{producto_id}/analisis", response_model=AnalisisCostos)
async def get_analisis_costos(
    producto_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar que el producto existe
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    query = db.query(Detalle_OC).join(
        Ordenes_Compra
    ).filter(
        Detalle_OC.ID_Producto == producto_id,
        Ordenes_Compra.Estado == 'Recibida'
    )
    
    if desde:
        query = query.filter(Ordenes_Compra.Fecha >= desde)
    if hasta:
        query = query.filter(Ordenes_Compra.Fecha <= hasta)
    
    # Análisis de costos
    analisis = db.query(
        func.min(Detalle_OC.Costo_Unitario).label('costo_minimo'),
        func.max(Detalle_OC.Costo_Unitario).label('costo_maximo'),
        func.avg(Detalle_OC.Costo_Unitario).label('costo_promedio'),
        func.sum(Detalle_OC.Cantidad).label('cantidad_total'),
        func.count(Detalle_OC.ID_Detalle_OC).label('cantidad_ordenes')
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).first()
    
    # Historial de costos
    historial = db.query(
        Ordenes_Compra.Fecha,
        Detalle_OC.Costo_Unitario,
        Detalle_OC.Cantidad,
        Ordenes_Compra.Numero_OC
    ).join(
        Ordenes_Compra
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).order_by(
        Ordenes_Compra.Fecha.desc()
    ).limit(10).all()
    
    # Stock actual
    stock_actual = db.query(func.sum(Inventario.Stock_Actual)).filter(
        Inventario.ID_Producto == producto_id
    ).scalar() or 0
    
    # Calcular variación porcentual entre primer y último costo
    costos_ordenados = db.query(
        Detalle_OC.Costo_Unitario,
        Ordenes_Compra.Fecha
    ).join(
        Ordenes_Compra
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).order_by(
        Ordenes_Compra.Fecha
    ).all()
    
    variacion_porcentual = 0
    if len(costos_ordenados) >= 2:
        primer_costo = costos_ordenados[0].Costo_Unitario
        ultimo_costo = costos_ordenados[-1].Costo_Unitario
        variacion_porcentual = ((ultimo_costo - primer_costo) / primer_costo * 100)
    
    return {
        "producto": {
            "id": producto.ID_Producto,
            "nombre": producto.Nombre,
            "codigo_barras": producto.Codigo_Barras,
            "sku": producto.SKU
        },
        "analisis": {
            "costo_minimo": analisis.costo_minimo,
            "costo_maximo": analisis.costo_maximo,
            "costo_promedio": round(analisis.costo_promedio, 2) if analisis.costo_promedio else 0,
            "cantidad_total": analisis.cantidad_total or 0,
            "cantidad_ordenes": analisis.cantidad_ordenes or 0,
            "variacion_porcentual": round(variacion_porcentual, 2),
            "stock_actual": stock_actual
        },
        "historial": [
            {
                "fecha": h.Fecha,
                "orden": h.Numero_OC,
                "costo": h.Costo_Unitario,
                "cantidad": h.Cantidad
            }
            for h in historial
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
