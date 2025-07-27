from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Sucursales_schema import (
    SucursalBase,
    SucursalCreate,
    SucursalUpdate,
    SucursalSimple,
    SucursalCompleta
)
from ..DB.Sucursales_model import Sucursales
from ..DB.Usuarios_model import Usuarios
from ..DB.Inventario_model import Inventario
from sqlalchemy import func, and_
from datetime import datetime, time
from sqlalchemy import case

router = APIRouter(
    prefix="/sucursales",
    tags=["Sucursales"]
)

# Obtener todas las sucursales con paginación y filtros
@router.get("/", response_model=List[SucursalSimple])
async def get_sucursales(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    provincia: Optional[str] = Query(None, description="Filtrar por provincia"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, dirección o localidad"),
    db: Session = Depends(get_db)
):
    query = db.query(Sucursales)
    
    if activo is not None:
        query = query.filter(Sucursales.Activo == activo)
    if provincia:
        query = query.filter(Sucursales.Provincia == provincia)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Sucursales.Nombre.ilike(search)) |
            (Sucursales.Direccion.ilike(search)) |
            (Sucursales.Localidad.ilike(search))
        )
    
    total = query.count()
    sucursales = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": sucursales,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una sucursal por ID
@router.get("/{sucursal_id}", response_model=SucursalCompleta)
async def get_sucursal(
    sucursal_id: int = Path(..., gt=0, description="ID de la sucursal"),
    db: Session = Depends(get_db)
):
    sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == sucursal_id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal

# Crear nueva sucursal
@router.post("/", response_model=SucursalCompleta)
async def create_sucursal(
    sucursal: SucursalCreate,
    db: Session = Depends(get_db)
):
    # Verificar nombre único
    existe_nombre = db.query(Sucursales).filter(Sucursales.Nombre == sucursal.nombre).first()
    if existe_nombre:
        raise HTTPException(status_code=400, detail="Ya existe una sucursal con este nombre")
    
    # Validar horarios
    if sucursal.horario_apertura and sucursal.horario_cierre:
        if sucursal.horario_apertura >= sucursal.horario_cierre:
            raise HTTPException(
                status_code=400,
                detail="El horario de apertura debe ser anterior al de cierre"
            )
    
    db_sucursal = Sucursales(
        Nombre=sucursal.nombre,
        Direccion=sucursal.direccion,
        Telefono=sucursal.telefono,
        Email=sucursal.email,
        Localidad=sucursal.localidad,
        Provincia=sucursal.provincia,
        Codigo_Postal=sucursal.codigo_postal,
        Horario_Apertura=sucursal.horario_apertura,
        Horario_Cierre=sucursal.horario_cierre
    )
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

# Actualizar sucursal
@router.put("/{sucursal_id}", response_model=SucursalCompleta)
async def update_sucursal(
    sucursal: SucursalUpdate,
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    db_sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == sucursal_id).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Verificar nombre único
    if sucursal.nombre:
        existe_nombre = db.query(Sucursales).filter(
            Sucursales.Nombre == sucursal.nombre,
            Sucursales.ID_Sucursal != sucursal_id
        ).first()
        if existe_nombre:
            raise HTTPException(status_code=400, detail="Ya existe una sucursal con este nombre")
    
    # Validar horarios
    horario_apertura = sucursal.horario_apertura or db_sucursal.Horario_Apertura
    horario_cierre = sucursal.horario_cierre or db_sucursal.Horario_Cierre
    if horario_apertura and horario_cierre and horario_apertura >= horario_cierre:
        raise HTTPException(
            status_code=400,
            detail="El horario de apertura debe ser anterior al de cierre"
        )
    
    # Actualizar campos
    for key, value in sucursal.dict(exclude_unset=True).items():
        setattr(db_sucursal, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_sucursal)
    return db_sucursal

# Eliminar sucursal (soft delete si tiene usuarios o inventario)
@router.delete("/{sucursal_id}")
async def delete_sucursal(
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    db_sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == sucursal_id).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Verificar si tiene usuarios asignados
    tiene_usuarios = db.query(func.count(Usuarios.ID_Usuario)).filter(
        Usuarios.ID_Sucursal == sucursal_id
    ).scalar()
    
    # Verificar si tiene inventario
    tiene_inventario = db.query(func.count(Inventario.ID_Inventario)).filter(
        Inventario.ID_Sucursal == sucursal_id
    ).scalar()
    
    if tiene_usuarios or tiene_inventario:
        # Soft delete
        db_sucursal.Activo = False
        db.commit()
        return {"message": "Sucursal desactivada porque tiene usuarios o inventario asociado"}
    else:
        # Hard delete
        db.delete(db_sucursal)
        db.commit()
        return {"message": "Sucursal eliminada"}

# Obtener usuarios de una sucursal
@router.get("/{sucursal_id}/usuarios", response_model=List[dict])
async def get_usuarios_sucursal(
    sucursal_id: int = Path(..., gt=0),
    activos: Optional[bool] = Query(None, description="Filtrar usuarios por estado activo"),
    db: Session = Depends(get_db)
):
    query = db.query(
        Usuarios.ID_Usuario,
        Usuarios.Nombre,
        Usuarios.Apellido,
        Usuarios.Email,
        Usuarios.Rol,
        Usuarios.Estado
    ).filter(Usuarios.ID_Sucursal == sucursal_id)
    
    if activos is not None:
        query = query.filter(Usuarios.Estado == activos)
    
    usuarios = query.all()
    return [
        {
            "id": u.ID_Usuario,
            "nombre": u.Nombre,
            "apellido": u.Apellido,
            "email": u.Email,
            "rol": u.Rol,
            "activo": u.Estado
        }
        for u in usuarios
    ]

# Obtener resumen de inventario de una sucursal
@router.get("/{sucursal_id}/inventario/resumen", response_model=dict)
async def get_resumen_inventario(
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Verificar que la sucursal existe
    sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == sucursal_id).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Obtener estadísticas de inventario
    stats = db.query(
        func.count(Inventario.ID_Inventario).label('total_productos'),
        func.sum(case((Inventario.Stock_Actual <= Inventario.Stock_Minimo, 1), else_=0)).label('productos_stock_bajo'),
        func.sum(case((Inventario.Stock_Actual >= Inventario.Stock_Maximo, 1), else_=0)).label('productos_stock_alto')
    ).filter(Inventario.ID_Sucursal == sucursal_id).first()
    
    return {
        "total_productos": stats.total_productos or 0,
        "productos_stock_bajo": stats.productos_stock_bajo or 0,
        "productos_stock_alto": stats.productos_stock_alto or 0,
        "nombre_sucursal": sucursal.Nombre,
        "ultima_actualizacion": datetime.now()
    }

# Obtener estadísticas generales de sucursales
@router.get("/estadisticas/general", response_model=dict)
async def get_estadisticas_sucursales(
    db: Session = Depends(get_db)
):
    total = db.query(func.count(Sucursales.ID_Sucursal)).scalar()
    activas = db.query(func.count(Sucursales.ID_Sucursal)).filter(Sucursales.Activo == True).scalar()
    
    # Sucursales por provincia
    por_provincia = db.query(
        Sucursales.Provincia,
        func.count(Sucursales.ID_Sucursal).label('total')
    ).group_by(Sucursales.Provincia).all()
    
    # Sucursales con más usuarios
    con_mas_usuarios = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        func.count(Usuarios.ID_Usuario).label('total_usuarios')
    ).join(Usuarios).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre
    ).order_by(func.count(Usuarios.ID_Usuario).desc()).limit(5).all()
    
    return {
        "total_sucursales": total,
        "sucursales_activas": activas,
        "por_provincia": [
            {"provincia": p.Provincia, "total": p.total}
            for p in por_provincia
        ],
        "con_mas_usuarios": [
            {
                "id": s.ID_Sucursal,
                "nombre": s.Nombre,
                "total_usuarios": s.total_usuarios
            }
            for s in con_mas_usuarios
        ]
    }
