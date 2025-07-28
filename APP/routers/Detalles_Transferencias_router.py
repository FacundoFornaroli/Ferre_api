from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Detalles_Transferencia_schema import (
    DetalleTransferenciaBase,
    DetalleTransferenciaCreate,
    DetalleTransferenciaUpdate,
    DetalleTransferenciaSimple,
    DetalleTransferenciaCompleto,
    SeguimientoDetalleTransferencia,
    AnalisisTransferenciasProducto
)
from APP.DB.Detalles_Transferencia_model import Detalles_Transferencia
from APP.DB.Transferencias_Sucursales_model import Transferencias_Sucursales
from APP.DB.Productos_model import Productos
from APP.DB.Inventario_model import Inventario
from APP.DB.Movimientos_inventario_model import Movimientos_inventario
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case, distinct, or_
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user
from APP.routers.Sucursales_router import Sucursales

router = APIRouter(
    prefix="/detalles-transferencia",
    tags=["Detalles de Transferencia"]
)

# Obtener detalles de una transferencia
@router.get("/transferencia/{transferencia_id}", response_model=List[DetalleTransferenciaCompleto])
async def get_detalles_transferencia(
    transferencia_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar transferencia y permisos
    transferencia = db.query(Transferencias_Sucursales).filter(
        Transferencias_Sucursales.ID_Transferencia == transferencia_id
    ).first()
    
    if not transferencia:
        raise HTTPException(status_code=404, detail="Transferencia no encontrada")
    
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal not in [
        transferencia.ID_Sucursal_Origen,
        transferencia.ID_Sucursal_Destino
    ]:
        raise HTTPException(status_code=403, detail="No tiene permisos para ver esta transferencia")
    
    detalles = db.query(
        Detalles_Transferencia,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU
    ).join(
        Productos
    ).filter(
        Detalles_Transferencia.ID_Transferencia == transferencia_id
    ).all()
    
    # Obtener stock actual en origen y destino
    resultados = []
    for detalle in detalles:
        stock_origen = db.query(Inventario.Stock_Actual).filter(
            Inventario.ID_Producto == detalle.Detalles_Transferencia.ID_Producto,
            Inventario.ID_Sucursal == transferencia.ID_Sucursal_Origen
        ).scalar() or 0
        
        stock_destino = db.query(Inventario.Stock_Actual).filter(
            Inventario.ID_Producto == detalle.Detalles_Transferencia.ID_Producto,
            Inventario.ID_Sucursal == transferencia.ID_Sucursal_Destino
        ).scalar() or 0
        
        resultados.append({
            "detalle": {
                "id_detalle": detalle.Detalles_Transferencia.ID_Detalle_Transferencia,
                "producto": {
                    "id": detalle.Detalles_Transferencia.ID_Producto,
                    "nombre": detalle.nombre_producto,
                    "codigo_barras": detalle.Codigo_Barras,
                    "sku": detalle.SKU
                },
                "cantidad": detalle.Detalles_Transferencia.Cantidad,
                "cantidad_recibida": detalle.Detalles_Transferencia.Cantidad_Recibida
            },
            "stock": {
                "origen": stock_origen,
                "destino": stock_destino
            },
            "estado": {
                "completado": detalle.Detalles_Transferencia.Cantidad_Recibida is not None,
                "diferencia": (detalle.Detalles_Transferencia.Cantidad_Recibida or 0) - detalle.Detalles_Transferencia.Cantidad
                if detalle.Detalles_Transferencia.Cantidad_Recibida is not None else None
            }
        })
    
    return resultados

# Actualizar cantidad recibida
@router.patch("/{detalle_id}/recepcion")
async def update_cantidad_recibida(
    detalle_id: int = Path(..., gt=0),
    cantidad_recibida: int = Query(..., gt=0),
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Obtener detalle y transferencia
    detalle = db.query(
        Detalles_Transferencia,
        Transferencias_Sucursales
    ).join(
        Transferencias_Sucursales
    ).filter(
        Detalles_Transferencia.ID_Detalle_Transferencia == detalle_id
    ).first()
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    # Verificar permisos
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal != detalle.Transferencias_Sucursales.ID_Sucursal_Destino:
        raise HTTPException(status_code=403, detail="Solo el destino puede confirmar la recepción")
    
    # Verificar estado de transferencia
    if detalle.Transferencias_Sucursales.Estado != "En Tránsito":
        raise HTTPException(status_code=400, detail="La transferencia debe estar en tránsito")
    
    if detalle.Detalles_Transferencia.Cantidad_Recibida is not None:
        raise HTTPException(status_code=400, detail="La cantidad recibida ya fue registrada")
    
    # Actualizar cantidad recibida
    detalle.Detalles_Transferencia.Cantidad_Recibida = cantidad_recibida
    
    # Verificar si todos los detalles fueron recibidos
    detalles_pendientes = db.query(Detalles_Transferencia).filter(
        Detalles_Transferencia.ID_Transferencia == detalle.Transferencias_Sucursales.ID_Transferencia,
        Detalles_Transferencia.Cantidad_Recibida.is_(None)
    ).count()
    
    if detalles_pendientes == 0:
        detalle.Transferencias_Sucursales.Estado = "Completada"
        if observaciones:
            detalle.Transferencias_Sucursales.Observaciones = (
                detalle.Transferencias_Sucursales.Observaciones or ""
            ) + f"\n[{datetime.now()}] Completada: {observaciones}"
    
    db.commit()
    
    return {
        "message": "Cantidad recibida actualizada",
        "transferencia_completada": detalles_pendientes == 0
    }

# Obtener seguimiento de un detalle
@router.get("/{detalle_id}/seguimiento", response_model=SeguimientoDetalleTransferencia)
async def get_seguimiento_detalle(
    detalle_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Obtener detalle y transferencia
    detalle = db.query(
        Detalles_Transferencia,
        Transferencias_Sucursales,
        Productos.Nombre.label('nombre_producto')
    ).join(
        Transferencias_Sucursales
    ).join(
        Productos
    ).filter(
        Detalles_Transferencia.ID_Detalle_Transferencia == detalle_id
    ).first()
    
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    
    # Verificar permisos
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal not in [
        detalle.Transferencias_Sucursales.ID_Sucursal_Origen,
        detalle.Transferencias_Sucursales.ID_Sucursal_Destino
    ]:
        raise HTTPException(status_code=403, detail="No tiene permisos para ver este detalle")
    
    # Obtener movimientos relacionados
    movimientos = db.query(Movimientos_inventario).filter(
        Movimientos_inventario.ID_Producto == detalle.Detalles_Transferencia.ID_Producto,
        Movimientos_inventario.Tipo == "Transferencia",
        Movimientos_inventario.ID_Referencia == detalle.Transferencias_Sucursales.ID_Transferencia
    ).order_by(
        Movimientos_inventario.Fecha
    ).all()
    
    return {
        "detalle": {
            "id_detalle": detalle.Detalles_Transferencia.ID_Detalle_Transferencia,
            "producto": {
                "id": detalle.Detalles_Transferencia.ID_Producto,
                "nombre": detalle.nombre_producto
            },
            "cantidad": detalle.Detalles_Transferencia.Cantidad,
            "cantidad_recibida": detalle.Detalles_Transferencia.Cantidad_Recibida
        },
        "transferencia": {
            "numero": detalle.Transferencias_Sucursales.Numero_Transferencia,
            "estado": detalle.Transferencias_Sucursales.Estado,
            "fecha_solicitud": detalle.Transferencias_Sucursales.Fecha_Solicitud,
            "fecha_transferencia": detalle.Transferencias_Sucursales.Fecha_Transferencia
        },
        "movimientos": [
            {
                "fecha": m.Fecha,
                "sucursal": m.ID_Sucursal,
                "tipo": "Salida" if m.Cantidad < 0 else "Entrada",
                "cantidad": abs(m.Cantidad)
            }
            for m in movimientos
        ]
    }

# Obtener análisis de transferencias por producto
@router.get("/producto/{producto_id}/analisis", response_model=AnalisisTransferenciasProducto)
async def get_analisis_producto(
    producto_id: int = Path(..., gt=0),
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
    
    # Verificar producto
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Análisis de transferencias
    transferencias = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        func.count(case([(Transferencias_Sucursales.ID_Sucursal_Origen == Sucursales.ID_Sucursal, 1)])).label('salidas'),
        func.sum(case([(Transferencias_Sucursales.ID_Sucursal_Origen == Sucursales.ID_Sucursal, Detalles_Transferencia.Cantidad)])).label('unidades_salida'),
        func.count(case([(Transferencias_Sucursales.ID_Sucursal_Destino == Sucursales.ID_Sucursal, 1)])).label('entradas'),
        func.sum(case([(Transferencias_Sucursales.ID_Sucursal_Destino == Sucursales.ID_Sucursal, Detalles_Transferencia.Cantidad)])).label('unidades_entrada')
    ).join(
        Transferencias_Sucursales,
        or_(
            Transferencias_Sucursales.ID_Sucursal_Origen == Sucursales.ID_Sucursal,
            Transferencias_Sucursales.ID_Sucursal_Destino == Sucursales.ID_Sucursal
        )
    ).join(
        Detalles_Transferencia,
        and_(
            Detalles_Transferencia.ID_Transferencia == Transferencias_Sucursales.ID_Transferencia,
            Detalles_Transferencia.ID_Producto == producto_id
        )
    ).filter(
        Transferencias_Sucursales.Estado != "Cancelada",
        Transferencias_Sucursales.Fecha_Solicitud.between(desde, hasta)
    ).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre
    ).all()
    
    # Stock actual por sucursal
    stock_actual = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Inventario.Stock_Actual
    ).join(
        Inventario,
        and_(
            Inventario.ID_Sucursal == Sucursales.ID_Sucursal,
            Inventario.ID_Producto == producto_id
        )
    ).filter(
        Inventario.Stock_Actual > 0
    ).all()
    
    return {
        "producto": {
            "id": producto.ID_Producto,
            "nombre": producto.Nombre,
            "codigo_barras": producto.Codigo_Barras,
            "sku": producto.SKU
        },
        "transferencias_por_sucursal": [
            {
                "sucursal": {
                    "id": t.ID_Sucursal,
                    "nombre": t.Nombre
                },
                "salidas": {
                    "cantidad": t.salidas or 0,
                    "unidades": t.unidades_salida or 0
                },
                "entradas": {
                    "cantidad": t.entradas or 0,
                    "unidades": t.unidades_entrada or 0
                }
            }
            for t in transferencias
        ],
        "stock_actual": [
            {
                "sucursal": {
                    "id": s.ID_Sucursal,
                    "nombre": s.Nombre
                },
                "stock": s.Stock_Actual
            }
            for s in stock_actual
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
