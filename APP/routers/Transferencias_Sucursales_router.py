from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Transferencias_Sucursales_schema import (
    TransferenciaSucursalBase,
    TransferenciaSucursalCreate,
    TransferenciaSucursalUpdate,
    TransferenciaSucursalSimple,
    TransferenciaSucursalCompleta,
    DetalleTransferenciaCreate,
    EstadisticasTransferencias
)
from APP.DB.Transferencias_Sucursales_model import Transferencias_Sucursales
from APP.DB.Detalles_Transferencia_model import Detalles_Transferencia
from APP.DB.Sucursales_model import Sucursales
from APP.DB.Productos_model import Productos
from APP.DB.Inventario_model import Inventario
from APP.DB.Movimientos_inventario_model import Movimientos_inventario
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case, distinct, or_
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/transferencias",
    tags=["Transferencias entre Sucursales"]
)

# Obtener todas las transferencias con filtros
@router.get("/", response_model=List[TransferenciaSucursalSimple])
async def get_transferencias(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    sucursal_origen: Optional[int] = Query(None, description="Filtrar por sucursal origen"),
    sucursal_destino: Optional[int] = Query(None, description="Filtrar por sucursal destino"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Transferencias_Sucursales,
        Sucursales.Nombre.label('nombre_origen'),
        func.count(Detalles_Transferencia.ID_Detalle_Transferencia).label('cantidad_items'),
        func.sum(Detalles_Transferencia.Cantidad).label('total_unidades')
    ).join(
        Sucursales,
        Sucursales.ID_Sucursal == Transferencias_Sucursales.ID_Sucursal_Origen
    ).join(
        Detalles_Transferencia
    ).group_by(
        Transferencias_Sucursales.ID_Transferencia,
        Sucursales.Nombre
    )
    
    # Aplicar filtros
    if estado:
        query = query.filter(Transferencias_Sucursales.Estado == estado)
    if sucursal_origen:
        query = query.filter(Transferencias_Sucursales.ID_Sucursal_Origen == sucursal_origen)
    if sucursal_destino:
        query = query.filter(Transferencias_Sucursales.ID_Sucursal_Destino == sucursal_destino)
    if desde:
        query = query.filter(Transferencias_Sucursales.Fecha_Solicitud >= desde)
    if hasta:
        query = query.filter(Transferencias_Sucursales.Fecha_Solicitud <= hasta)
    
    # Filtrar por permisos de usuario
    if current_user.Rol not in ["Admin", "Supervisor"]:
        query = query.filter(
            or_(
                Transferencias_Sucursales.ID_Sucursal_Origen == current_user.ID_Sucursal,
                Transferencias_Sucursales.ID_Sucursal_Destino == current_user.ID_Sucursal
            )
        )
    
    total = query.count()
    transferencias = query.order_by(Transferencias_Sucursales.Fecha_Solicitud.desc()).offset(skip).limit(limit).all()
    
    # Obtener nombres de sucursales destino
    sucursales_destino = {
        s.ID_Sucursal: s.Nombre for s in db.query(Sucursales).filter(
            Sucursales.ID_Sucursal.in_([t.Transferencias_Sucursales.ID_Sucursal_Destino for t in transferencias])
        ).all()
    }
    
    return {
        "total": total,
        "items": [
            {
                "id_transferencia": t.Transferencias_Sucursales.ID_Transferencia,
                "numero": t.Transferencias_Sucursales.Numero_Transferencia,
                "sucursal_origen": {
                    "id": t.Transferencias_Sucursales.ID_Sucursal_Origen,
                    "nombre": t.nombre_origen
                },
                "sucursal_destino": {
                    "id": t.Transferencias_Sucursales.ID_Sucursal_Destino,
                    "nombre": sucursales_destino[t.Transferencias_Sucursales.ID_Sucursal_Destino]
                },
                "fecha_solicitud": t.Transferencias_Sucursales.Fecha_Solicitud,
                "fecha_transferencia": t.Transferencias_Sucursales.Fecha_Transferencia,
                "estado": t.Transferencias_Sucursales.Estado,
                "items": t.cantidad_items,
                "unidades": t.total_unidades
            }
            for t in transferencias
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una transferencia específica
@router.get("/{transferencia_id}", response_model=TransferenciaSucursalCompleta)
async def get_transferencia(
    transferencia_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    transferencia = db.query(
        Transferencias_Sucursales,
        Sucursales.Nombre.label('nombre_origen')
    ).join(
        Sucursales,
        Sucursales.ID_Sucursal == Transferencias_Sucursales.ID_Sucursal_Origen
    ).filter(
        Transferencias_Sucursales.ID_Transferencia == transferencia_id
    ).first()
    
    if not transferencia:
        raise HTTPException(status_code=404, detail="Transferencia no encontrada")
    
    # Verificar permisos
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal not in [
        transferencia.Transferencias_Sucursales.ID_Sucursal_Origen,
        transferencia.Transferencias_Sucursales.ID_Sucursal_Destino
    ]:
        raise HTTPException(status_code=403, detail="No tiene permisos para ver esta transferencia")
    
    # Obtener detalles
    detalles = db.query(
        Detalles_Transferencia,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Inventario.Stock_Actual.label('stock_origen')
    ).join(
        Productos
    ).outerjoin(
        Inventario,
        and_(
            Inventario.ID_Producto == Productos.ID_Producto,
            Inventario.ID_Sucursal == transferencia.Transferencias_Sucursales.ID_Sucursal_Origen
        )
    ).filter(
        Detalles_Transferencia.ID_Transferencia == transferencia_id
    ).all()
    
    # Obtener nombres de usuarios
    usuarios = db.query(Usuarios).filter(
        Usuarios.ID_Usuario.in_([
            transferencia.Transferencias_Sucursales.ID_Usuario_Solicitante,
            transferencia.Transferencias_Sucursales.ID_Usuario_Autorizador
        ])
    ).all()
    usuarios_dict = {u.ID_Usuario: f"{u.Nombre} {u.Apellido}" for u in usuarios}
    
    return {
        "transferencia": {
            "id_transferencia": transferencia.Transferencias_Sucursales.ID_Transferencia,
            "numero": transferencia.Transferencias_Sucursales.Numero_Transferencia,
            "sucursal_origen": {
                "id": transferencia.Transferencias_Sucursales.ID_Sucursal_Origen,
                "nombre": transferencia.nombre_origen
            },
            "sucursal_destino": {
                "id": transferencia.Transferencias_Sucursales.ID_Sucursal_Destino,
                "nombre": db.query(Sucursales.Nombre).filter(
                    Sucursales.ID_Sucursal == transferencia.Transferencias_Sucursales.ID_Sucursal_Destino
                ).scalar()
            },
            "fecha_solicitud": transferencia.Transferencias_Sucursales.Fecha_Solicitud,
            "fecha_transferencia": transferencia.Transferencias_Sucursales.Fecha_Transferencia,
            "estado": transferencia.Transferencias_Sucursales.Estado,
            "usuarios": {
                "solicitante": usuarios_dict.get(transferencia.Transferencias_Sucursales.ID_Usuario_Solicitante),
                "autorizador": usuarios_dict.get(transferencia.Transferencias_Sucursales.ID_Usuario_Autorizador)
            },
            "observaciones": transferencia.Transferencias_Sucursales.Observaciones
        },
        "detalles": [
            {
                "producto": {
                    "id": d.Detalles_Transferencia.ID_Producto,
                    "nombre": d.nombre_producto,
                    "codigo_barras": d.Codigo_Barras
                },
                "cantidad": d.Detalles_Transferencia.Cantidad,
                "cantidad_recibida": d.Detalles_Transferencia.Cantidad_Recibida,
                "stock_origen": d.stock_origen or 0
            }
            for d in detalles
        ]
    }

# Crear nueva transferencia
@router.post("/", response_model=TransferenciaSucursalCompleta)
async def create_transferencia(
    transferencia: TransferenciaSucursalCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar sucursales
    if transferencia.id_sucursal_origen == transferencia.id_sucursal_destino:
        raise HTTPException(
            status_code=400,
            detail="La sucursal origen y destino no pueden ser la misma"
        )
    
    # Verificar permisos
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal != transferencia.id_sucursal_origen:
        raise HTTPException(
            status_code=403,
            detail="Solo puede crear transferencias desde su sucursal"
        )
    
    # Verificar stock disponible
    for detalle in transferencia.detalles:
        stock = db.query(Inventario).filter(
            Inventario.ID_Producto == detalle.id_producto,
            Inventario.ID_Sucursal == transferencia.id_sucursal_origen
        ).first()
        
        if not stock or stock.Stock_Actual < detalle.cantidad:
            producto = db.query(Productos).filter(Productos.ID_Producto == detalle.id_producto).first()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para el producto {producto.Nombre}"
            )
    
    # Crear transferencia
    db_transferencia = Transferencias_Sucursales(
        ID_Sucursal_Origen=transferencia.id_sucursal_origen,
        ID_Sucursal_Destino=transferencia.id_sucursal_destino,
        Estado="Pendiente",
        ID_Usuario_Solicitante=current_user.ID_Usuario,
        Observaciones=transferencia.observaciones
    )
    db.add(db_transferencia)
    db.flush()
    
    # Crear detalles
    for detalle in transferencia.detalles:
        db_detalle = Detalles_Transferencia(
            ID_Transferencia=db_transferencia.ID_Transferencia,
            ID_Producto=detalle.id_producto,
            Cantidad=detalle.cantidad
        )
        db.add(db_detalle)
    
    db.commit()
    db.refresh(db_transferencia)
    
    return await get_transferencia(db_transferencia.ID_Transferencia, db, current_user)

# Actualizar estado de transferencia
@router.patch("/{transferencia_id}/estado")
async def update_estado_transferencia(
    transferencia_id: int = Path(..., gt=0),
    estado: str = Query(..., description="Nuevo estado de la transferencia"),
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    transferencia = db.query(Transferencias_Sucursales).filter(
        Transferencias_Sucursales.ID_Transferencia == transferencia_id
    ).first()
    
    if not transferencia:
        raise HTTPException(status_code=404, detail="Transferencia no encontrada")
    
    # Verificar permisos
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Sucursal not in [
        transferencia.ID_Sucursal_Origen,
        transferencia.ID_Sucursal_Destino
    ]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    estados_validos = {
        "Pendiente": ["Aprobada", "Cancelada"],
        "Aprobada": ["En Tránsito", "Cancelada"],
        "En Tránsito": ["Completada", "Cancelada"],
        "Completada": [],
        "Cancelada": []
    }
    
    if estado not in estados_validos.get(transferencia.Estado, []):
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar el estado de {transferencia.Estado} a {estado}"
        )
    
    # Procesar cambio de estado
    if estado == "Aprobada":
        transferencia.ID_Usuario_Autorizador = current_user.ID_Usuario
        transferencia.Fecha_Transferencia = datetime.now()
        
        # Verificar stock nuevamente
        detalles = db.query(Detalles_Transferencia).filter(
            Detalles_Transferencia.ID_Transferencia == transferencia_id
        ).all()
        
        for detalle in detalles:
            stock = db.query(Inventario).filter(
                Inventario.ID_Producto == detalle.ID_Producto,
                Inventario.ID_Sucursal == transferencia.ID_Sucursal_Origen
            ).first()
            
            if not stock or stock.Stock_Actual < detalle.Cantidad:
                producto = db.query(Productos).filter(Productos.ID_Producto == detalle.ID_Producto).first()
                raise HTTPException(
                    status_code=400,
                    detail=f"Stock insuficiente para el producto {producto.Nombre}"
                )
    
    elif estado == "Completada":
        detalles = db.query(Detalles_Transferencia).filter(
            Detalles_Transferencia.ID_Transferencia == transferencia_id
        ).all()
        
        for detalle in detalles:
            # Reducir stock en origen
            stock_origen = db.query(Inventario).filter(
                Inventario.ID_Producto == detalle.ID_Producto,
                Inventario.ID_Sucursal == transferencia.ID_Sucursal_Origen
            ).first()
            
            stock_origen.Stock_Actual -= detalle.Cantidad
            stock_origen.Fecha_Ultimo_Movimiento = datetime.now()
            
            # Registrar movimiento en origen
            movimiento_origen = Movimientos_inventario(
                ID_Producto=detalle.ID_Producto,
                ID_Sucursal=transferencia.ID_Sucursal_Origen,
                Tipo="Transferencia",
                Cantidad=-detalle.Cantidad,
                ID_Usuario=current_user.ID_Usuario,
                ID_Referencia=transferencia_id,
                Tipo_Referencia="Transferencia",
                Observaciones=f"Transferencia #{transferencia.Numero_Transferencia} - Salida"
            )
            db.add(movimiento_origen)
            
            # Actualizar o crear stock en destino
            stock_destino = db.query(Inventario).filter(
                Inventario.ID_Producto == detalle.ID_Producto,
                Inventario.ID_Sucursal == transferencia.ID_Sucursal_Destino
            ).first()
            
            if not stock_destino:
                stock_destino = Inventario(
                    ID_Producto=detalle.ID_Producto,
                    ID_Sucursal=transferencia.ID_Sucursal_Destino,
                    Stock_Actual=0,
                    Stock_Minimo=0,
                    Stock_Maximo=999999
                )
                db.add(stock_destino)
                db.flush()
            
            stock_destino.Stock_Actual += detalle.Cantidad
            stock_destino.Fecha_Ultimo_Movimiento = datetime.now()
            
            # Registrar movimiento en destino
            movimiento_destino = Movimientos_inventario(
                ID_Producto=detalle.ID_Producto,
                ID_Sucursal=transferencia.ID_Sucursal_Destino,
                Tipo="Transferencia",
                Cantidad=detalle.Cantidad,
                ID_Usuario=current_user.ID_Usuario,
                ID_Referencia=transferencia_id,
                Tipo_Referencia="Transferencia",
                Observaciones=f"Transferencia #{transferencia.Numero_Transferencia} - Entrada"
            )
            db.add(movimiento_destino)
    
    # Actualizar estado
    transferencia.Estado = estado
    if observaciones:
        transferencia.Observaciones = (transferencia.Observaciones or "") + f"\n[{datetime.now()}] {estado}: {observaciones}"
    
    db.commit()
    
    return {"message": f"Estado actualizado a {estado}"}

# Obtener estadísticas de transferencias
@router.get("/estadisticas", response_model=EstadisticasTransferencias)
async def get_estadisticas_transferencias(
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
    
    # Transferencias por estado
    por_estado = db.query(
        Transferencias_Sucursales.Estado,
        func.count(Transferencias_Sucursales.ID_Transferencia).label('total'),
        func.count(distinct(Detalles_Transferencia.ID_Producto)).label('productos_distintos'),
        func.sum(Detalles_Transferencia.Cantidad).label('unidades')
    ).join(
        Detalles_Transferencia
    ).filter(
        Transferencias_Sucursales.Fecha_Solicitud.between(desde, hasta)
    ).group_by(
        Transferencias_Sucursales.Estado
    ).all()
    
    # Transferencias por sucursal
    por_sucursal = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        func.count(case([(Transferencias_Sucursales.ID_Sucursal_Origen == Sucursales.ID_Sucursal, 1)])).label('salidas'),
        func.count(case([(Transferencias_Sucursales.ID_Sucursal_Destino == Sucursales.ID_Sucursal, 1)])).label('entradas')
    ).outerjoin(
        Transferencias_Sucursales,
        or_(
            Transferencias_Sucursales.ID_Sucursal_Origen == Sucursales.ID_Sucursal,
            Transferencias_Sucursales.ID_Sucursal_Destino == Sucursales.ID_Sucursal
        )
    ).filter(
        Transferencias_Sucursales.Fecha_Solicitud.between(desde, hasta)
    ).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre
    ).all()
    
    # Productos más transferidos
    productos_transferidos = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        func.count(Detalles_Transferencia.ID_Detalle_Transferencia).label('transferencias'),
        func.sum(Detalles_Transferencia.Cantidad).label('unidades')
    ).join(
        Detalles_Transferencia
    ).join(
        Transferencias_Sucursales,
        and_(
            Transferencias_Sucursales.ID_Transferencia == Detalles_Transferencia.ID_Transferencia,
            Transferencias_Sucursales.Estado != 'Cancelada',
            Transferencias_Sucursales.Fecha_Solicitud.between(desde, hasta)
        )
    ).group_by(
        Productos.ID_Producto,
        Productos.Nombre
    ).order_by(
        func.sum(Detalles_Transferencia.Cantidad).desc()
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
        "por_sucursal": [
            {
                "sucursal": {
                    "id": s.ID_Sucursal,
                    "nombre": s.Nombre
                },
                "salidas": s.salidas,
                "entradas": s.entradas,
                "total": s.salidas + s.entradas
            }
            for s in por_sucursal
        ],
        "productos_mas_transferidos": [
            {
                "producto": {
                    "id": p.ID_Producto,
                    "nombre": p.Nombre
                },
                "transferencias": p.transferencias,
                "unidades": p.unidades
            }
            for p in productos_transferidos
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
