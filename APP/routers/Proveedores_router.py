from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Proveedores_schema import (
    ProveedorBase,
    ProveedorCreate,
    ProveedorUpdate,
    ProveedorSimple,
    ProveedorCompleta
)
from APP.DB.Proveedores_model import Proveedores
from APP.DB.Ordenes_Compra_model import Ordenes_Compra
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/proveedores",
    tags=["Proveedores"]
)

# Obtener todos los proveedores con paginación y filtros
@router.get("/", response_model=List[ProveedorSimple])
async def get_proveedores(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    provincia: Optional[str] = Query(None, description="Filtrar por provincia"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, CUIT o email"),
    ordenar_por: Optional[str] = Query(None, description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(Proveedores)
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Proveedores.Activo == activo)
    if provincia:
        query = query.filter(Proveedores.Provincia == provincia)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Proveedores.Nombre.ilike(search)) |
            (Proveedores.CUIT.ilike(search)) |
            (Proveedores.Email.ilike(search))
        )
    
    # Aplicar ordenamiento
    if ordenar_por:
        orden_col = getattr(Proveedores, ordenar_por.capitalize(), Proveedores.Nombre)
        if orden == "desc":
            orden_col = orden_col.desc()
        query = query.order_by(orden_col)
    
    total = query.count()
    proveedores = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": proveedores,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener un proveedor por ID
@router.get("/{proveedor_id}", response_model=ProveedorCompleta)
async def get_proveedor(
    proveedor_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    proveedor = db.query(Proveedores).filter(Proveedores.ID_Proveedor == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return proveedor

# Crear nuevo proveedor
@router.post("/", response_model=ProveedorCompleta)
async def create_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar CUIT único si se proporciona
    if proveedor.cuit:
        existe_cuit = db.query(Proveedores).filter(Proveedores.CUIT == proveedor.cuit).first()
        if existe_cuit:
            raise HTTPException(status_code=400, detail="CUIT ya registrado")
    
    # Verificar email único si se proporciona
    if proveedor.email:
        existe_email = db.query(Proveedores).filter(Proveedores.Email == proveedor.email).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Validar plazo de entrega
    if proveedor.plazo_entrega is not None and proveedor.plazo_entrega < 0:
        raise HTTPException(status_code=400, detail="El plazo de entrega no puede ser negativo")
    
    # Crear proveedor
    db_proveedor = Proveedores(**proveedor.dict())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Actualizar proveedor
@router.put("/{proveedor_id}", response_model=ProveedorCompleta)
async def update_proveedor(
    proveedor: ProveedorUpdate,
    proveedor_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_proveedor = db.query(Proveedores).filter(Proveedores.ID_Proveedor == proveedor_id).first()
    if not db_proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Verificar CUIT único
    if proveedor.cuit and proveedor.cuit != db_proveedor.CUIT:
        existe_cuit = db.query(Proveedores).filter(
            Proveedores.CUIT == proveedor.cuit,
            Proveedores.ID_Proveedor != proveedor_id
        ).first()
        if existe_cuit:
            raise HTTPException(status_code=400, detail="CUIT ya registrado")
    
    # Verificar email único
    if proveedor.email and proveedor.email != db_proveedor.Email:
        existe_email = db.query(Proveedores).filter(
            Proveedores.Email == proveedor.email,
            Proveedores.ID_Proveedor != proveedor_id
        ).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Validar plazo de entrega
    if proveedor.plazo_entrega is not None and proveedor.plazo_entrega < 0:
        raise HTTPException(status_code=400, detail="El plazo de entrega no puede ser negativo")
    
    # Actualizar campos
    for key, value in proveedor.dict(exclude_unset=True).items():
        setattr(db_proveedor, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_proveedor)
    return db_proveedor

# Obtener historial de órdenes de compra
@router.get("/{proveedor_id}/ordenes", response_model=List[dict])
async def get_historial_ordenes(
    proveedor_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Ordenes_Compra.ID_OC,
        Ordenes_Compra.Numero_OC,
        Ordenes_Compra.Fecha,
        Ordenes_Compra.Fecha_Entrega_Esperada,
        Ordenes_Compra.Total,
        Ordenes_Compra.Estado
    ).filter(Ordenes_Compra.ID_Proveedor == proveedor_id)
    
    if desde:
        query = query.filter(Ordenes_Compra.Fecha >= desde)
    if hasta:
        query = query.filter(Ordenes_Compra.Fecha <= hasta)
    if estado:
        query = query.filter(Ordenes_Compra.Estado == estado)
    
    ordenes = query.order_by(Ordenes_Compra.Fecha.desc()).all()
    
    return [
        {
            "id": o.ID_OC,
            "numero_oc": o.Numero_OC,
            "fecha": o.Fecha,
            "fecha_entrega": o.Fecha_Entrega_Esperada,
            "total": o.Total,
            "estado": o.Estado,
            "dias_restantes": (o.Fecha_Entrega_Esperada - datetime.now().date()).days
            if o.Fecha_Entrega_Esperada and o.Estado not in ['Recibida', 'Cancelada']
            else None
        }
        for o in ordenes
    ]

# Obtener estadísticas del proveedor
@router.get("/{proveedor_id}/estadisticas", response_model=dict)
async def get_estadisticas_proveedor(
    proveedor_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    proveedor = db.query(Proveedores).filter(Proveedores.ID_Proveedor == proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Órdenes pendientes
    ordenes_pendientes = db.query(
        func.count(Ordenes_Compra.ID_OC).label('cantidad'),
        func.sum(Ordenes_Compra.Total).label('total')
    ).filter(
        Ordenes_Compra.ID_Proveedor == proveedor_id,
        Ordenes_Compra.Estado.in_(['Pendiente', 'Aprobada'])
    ).first()
    
    # Tiempo promedio de entrega
    tiempo_entrega = db.query(
        func.avg(
            func.datediff(
                'day',
                Ordenes_Compra.Fecha,
                Ordenes_Compra.Fecha_Entrega_Esperada
            )
        ).label('promedio_dias')
    ).filter(
        Ordenes_Compra.ID_Proveedor == proveedor_id,
        Ordenes_Compra.Estado == 'Recibida'
    ).first()
    
    # Últimas órdenes
    ultimas_ordenes = db.query(
        func.count(Ordenes_Compra.ID_OC).label('total'),
        func.sum(case((Ordenes_Compra.Fecha >= datetime.now() - timedelta(days=30), 1), else_=0)).label('ultimo_mes'),
        func.sum(Ordenes_Compra.Total).label('monto_total')
    ).filter(
        Ordenes_Compra.ID_Proveedor == proveedor_id,
        Ordenes_Compra.Estado != 'Cancelada'
    ).first()
    
    return {
        "ordenes_pendientes": {
            "cantidad": ordenes_pendientes.cantidad or 0,
            "total": ordenes_pendientes.total or 0
        },
        "tiempo_entrega": {
            "promedio_dias": round(tiempo_entrega.promedio_dias or 0, 1),
            "plazo_establecido": proveedor.Plazo_Entrega
        },
        "estadisticas_ordenes": {
            "total_ordenes": ultimas_ordenes.total or 0,
            "ordenes_ultimo_mes": ultimas_ordenes.ultimo_mes or 0,
            "monto_total": ultimas_ordenes.monto_total or 0
        }
    }

# Obtener estadísticas generales de proveedores
@router.get("/estadisticas/general", response_model=dict)
async def get_estadisticas_proveedores(
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    total = db.query(func.count(Proveedores.ID_Proveedor)).scalar()
    activos = db.query(func.count(Proveedores.ID_Proveedor)).filter(
        Proveedores.Activo == True
    ).scalar()
    
    # Proveedores por provincia
    por_provincia = db.query(
        Proveedores.Provincia,
        func.count(Proveedores.ID_Proveedor).label('total')
    ).group_by(Proveedores.Provincia).all()
    
    # Mejores proveedores (por monto de órdenes)
    mejores_proveedores = db.query(
        Proveedores.ID_Proveedor,
        Proveedores.Nombre,
        func.count(Ordenes_Compra.ID_OC).label('total_ordenes'),
        func.sum(Ordenes_Compra.Total).label('monto_total'),
        func.avg(
            func.datediff(
                'day',
                Ordenes_Compra.Fecha,
                Ordenes_Compra.Fecha_Entrega_Esperada
            )
        ).label('promedio_entrega')
    ).join(Ordenes_Compra).filter(
        Ordenes_Compra.Estado != 'Cancelada'
    ).group_by(
        Proveedores.ID_Proveedor,
        Proveedores.Nombre
    ).order_by(func.sum(Ordenes_Compra.Total).desc()).limit(5).all()
    
    return {
        "total_proveedores": total,
        "proveedores_activos": activos,
        "por_provincia": [
            {"provincia": p.Provincia, "total": p.total}
            for p in por_provincia
        ],
        "mejores_proveedores": [
            {
                "id": p.ID_Proveedor,
                "nombre": p.Nombre,
                "total_ordenes": p.total_ordenes,
                "monto_total": p.monto_total,
                "promedio_entrega": round(p.promedio_entrega or 0, 1)
            }
            for p in mejores_proveedores
        ]
    }