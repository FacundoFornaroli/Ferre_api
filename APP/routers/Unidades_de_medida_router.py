from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Unidades_de_medida_schema import (
    Unidad_de_medida_base,
    Unidad_de_medida_create,
    Unidad_de_medida_update,
    Unidad_de_medida_simple,
    Unidad_de_medida_completa
)
from ..DB.Unidades_de_medida_model import Unidades_de_medida
from sqlalchemy import func
from ..DB.Productos_model import Productos

router = APIRouter(
    prefix="/unidades-medida",
    tags=["Unidades de Medida"]
)

# Obtener todas las unidades con paginación y filtros
@router.get("/", response_model=List[Unidad_de_medida_simple])
async def get_unidades_medida(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o abreviatura"),
    db: Session = Depends(get_db)
):
    query = db.query(Unidades_de_medida)
    
    if activo is not None:
        query = query.filter(Unidades_de_medida.Activo == activo)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Unidades_de_medida.Nombre.ilike(search)) |
            (Unidades_de_medida.Abreviatura.ilike(search))
        )
    
    total = query.count()
    unidades = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": unidades,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una unidad por ID
@router.get("/{unidad_id}", response_model=Unidad_de_medida_completa)
async def get_unidad_medida(
    unidad_id: int = Path(..., gt=0, description="ID de la unidad de medida"),
    db: Session = Depends(get_db)
):
    unidad = db.query(Unidades_de_medida).filter(Unidades_de_medida.ID_Unidad_de_medida == unidad_id).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    return unidad

# Crear nueva unidad
@router.post("/", response_model=Unidad_de_medida_completa)
async def create_unidad_medida(
    unidad: Unidad_de_medida_create,
    db: Session = Depends(get_db)
):
    # Verificar nombre único
    existe_nombre = db.query(Unidades_de_medida).filter(Unidades_de_medida.Nombre == unidad.nombre).first()
    if existe_nombre:
        raise HTTPException(status_code=400, detail="Ya existe una unidad con este nombre")
    
    # Verificar abreviatura única
    existe_abrev = db.query(Unidades_de_medida).filter(Unidades_de_medida.Abreviatura == unidad.abreviatura).first()
    if existe_abrev:
        raise HTTPException(status_code=400, detail="Ya existe una unidad con esta abreviatura")
    
    db_unidad = Unidades_de_medida(
        Nombre=unidad.nombre,
        Abreviatura=unidad.abreviatura
    )
    db.add(db_unidad)
    db.commit()
    db.refresh(db_unidad)
    return db_unidad

# Actualizar unidad
@router.put("/{unidad_id}", response_model=Unidad_de_medida_completa)
async def update_unidad_medida(
    unidad: Unidad_de_medida_update,
    unidad_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    db_unidad = db.query(Unidades_de_medida).filter(Unidades_de_medida.ID_Unidad_de_medida == unidad_id).first()
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    # Verificar nombre único si se está actualizando
    if unidad.nombre:
        existe_nombre = db.query(Unidades_de_medida).filter(
            Unidades_de_medida.Nombre == unidad.nombre,
            Unidades_de_medida.ID_Unidad_de_medida != unidad_id
        ).first()
        if existe_nombre:
            raise HTTPException(status_code=400, detail="Ya existe una unidad con este nombre")
    
    # Verificar abreviatura única si se está actualizando
    if unidad.abreviatura:
        existe_abrev = db.query(Unidades_de_medida).filter(
            Unidades_de_medida.Abreviatura == unidad.abreviatura,
            Unidades_de_medida.ID_Unidad_de_medida != unidad_id
        ).first()
        if existe_abrev:
            raise HTTPException(status_code=400, detail="Ya existe una unidad con esta abreviatura")
    
    # Actualizar campos
    for key, value in unidad.dict(exclude_unset=True).items():
        setattr(db_unidad, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_unidad)
    return db_unidad

# Eliminar unidad (soft delete si tiene productos asociados)
@router.delete("/{unidad_id}")
async def delete_unidad_medida(
    unidad_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    db_unidad = db.query(Unidades_de_medida).filter(Unidades_de_medida.ID_Unidad_de_medida == unidad_id).first()
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    # Verificar si tiene productos asociados
    tiene_productos = db.query(func.count()).select_from(Productos).filter(
        Productos.ID_Unidad_de_medida == unidad_id
    ).scalar()
    
    if tiene_productos:
        # Soft delete
        db_unidad.Activo = False
        db.commit()
        return {"message": "Unidad de medida desactivada porque tiene productos asociados"}
    else:
        # Hard delete si no tiene productos
        db.delete(db_unidad)
        db.commit()
        return {"message": "Unidad de medida eliminada"}

# Obtener estadísticas
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_unidades(
    db: Session = Depends(get_db)
):
    total = db.query(func.count(Unidades_de_medida.ID_Unidad_de_medida)).scalar()
    activas = db.query(func.count(Unidades_de_medida.ID_Unidad_de_medida)).filter(
        Unidades_de_medida.Activo == True
    ).scalar()
    
    # Unidades más usadas
    mas_usadas = db.query(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura,
        func.count(Productos.ID_Producto).label('total_productos')
    ).join(Productos).group_by(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura
    ).order_by(func.count(Productos.ID_Producto).desc()).limit(5).all()
    
    return {
        "total_unidades": total,
        "unidades_activas": activas,
        "mas_usadas": [
            {
                "id": u.ID_Unidad_de_medida,
                "nombre": u.Nombre,
                "abreviatura": u.Abreviatura,
                "total_productos": u.total_productos
            }
            for u in mas_usadas
        ]
    }
