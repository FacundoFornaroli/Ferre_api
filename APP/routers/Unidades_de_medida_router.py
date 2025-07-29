from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Unidades_de_medida_schema import (
    UnidadMedidaBase,
    UnidadMedidaCreate,
    UnidadMedidaUpdate,
    UnidadMedidaSimple,
    UnidadMedidaCompleta,
    UnidadMedidaList
)
from APP.DB.Unidades_de_medida_model import Unidades_de_medida
from sqlalchemy import func, and_
from APP.DB.Productos_model import Productos

router = APIRouter(
    prefix="/unidades-medida",
    tags=["Unidades de Medida"]
)

# Obtener todas las unidades de medida con paginación y filtros
@router.get("/", response_model=UnidadMedidaList)
async def get_unidades_medida(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o abreviatura"),
    ordenar_por: Optional[str] = Query("nombre", description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    # Query base con conteo de productos
    query = db.query(
        Unidades_de_medida,
        func.count(Productos.ID_Producto).label('productos_count')
    ).outerjoin(
        Productos, and_(
            Productos.ID_Unidad_de_medida == Unidades_de_medida.ID_Unidad_de_medida,
            Productos.Activo == True
        )
    ).group_by(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura,
        Unidades_de_medida.Activo
    )
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Unidades_de_medida.Activo == activo)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Unidades_de_medida.Nombre.ilike(search)) |
            (Unidades_de_medida.Abreviatura.ilike(search))
        )
    
    # Contar total de registros
    total = db.query(func.count(Unidades_de_medida.ID_Unidad_de_medida)).scalar()
    
    # Aplicar ordenamiento
    if ordenar_por == "nombre":
        if orden == "desc":
            query = query.order_by(Unidades_de_medida.Nombre.desc())
        else:
            query = query.order_by(Unidades_de_medida.Nombre.asc())
    elif ordenar_por == "abreviatura":
        if orden == "desc":
            query = query.order_by(Unidades_de_medida.Abreviatura.desc())
        else:
            query = query.order_by(Unidades_de_medida.Abreviatura.asc())
    else:
        query = query.order_by(Unidades_de_medida.Nombre.asc())
    
    # Aplicar paginación
    resultados = query.offset(skip).limit(limit).all()
    
    # Procesar resultados
    unidades_procesadas = []
    for unidad, productos_count in resultados:
        unidad_dict = {
            "id_unidad_medida": unidad.ID_Unidad_de_medida,
            "nombre": unidad.Nombre,
            "abreviatura": unidad.Abreviatura,
            "activo": unidad.Activo,
            "productos_count": productos_count
        }
        unidades_procesadas.append(unidad_dict)
    
    return {
        "total_registros": total,
        "pagina_actual": skip // limit + 1,
        "total_paginas": (total + limit - 1) // limit,
        "unidades": unidades_procesadas
    }

# Obtener estadísticas de unidades de medida
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_unidades_medida(
    db: Session = Depends(get_db)
):
    # Total de unidades
    total_unidades = db.query(func.count(Unidades_de_medida.ID_Unidad_de_medida)).scalar()
    
    # Unidades activas
    unidades_activas = db.query(func.count(Unidades_de_medida.ID_Unidad_de_medida)).filter(
        Unidades_de_medida.Activo == True
    ).scalar()
    
    # Unidades más usadas
    unidades_productos = db.query(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura,
        func.count(Productos.ID_Producto).label('total_productos')
    ).join(
        Productos, and_(
            Productos.ID_Unidad_de_medida == Unidades_de_medida.ID_Unidad_de_medida,
            Productos.Activo == True
        )
    ).group_by(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura
    ).order_by(
        func.count(Productos.ID_Producto).desc()
    ).limit(5).all()
    
    return {
        "total_unidades": total_unidades,
        "unidades_activas": unidades_activas,
        "unidades_mas_usadas": [
            {
                "id": unidad.ID_Unidad_de_medida,
                "nombre": unidad.Nombre,
                "abreviatura": unidad.Abreviatura,
                "total_productos": unidad.total_productos
            }
            for unidad in unidades_productos
        ]
    }

# Obtener una unidad de medida por ID
@router.get("/{unidad_id}", response_model=UnidadMedidaCompleta)
async def get_unidad_medida(
    unidad_id: int = Path(..., gt=0, description="ID de la unidad de medida"),
    db: Session = Depends(get_db)
):
    # Query con conteo de productos
    result = db.query(
        Unidades_de_medida,
        func.count(Productos.ID_Producto).label('productos_count')
    ).outerjoin(
        Productos, and_(
            Productos.ID_Unidad_de_medida == Unidades_de_medida.ID_Unidad_de_medida,
            Productos.Activo == True
        )
    ).filter(
        Unidades_de_medida.ID_Unidad_de_medida == unidad_id
    ).group_by(
        Unidades_de_medida.ID_Unidad_de_medida,
        Unidades_de_medida.Nombre,
        Unidades_de_medida.Abreviatura,
        Unidades_de_medida.Activo
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    unidad, productos_count = result
    
    return {
        "id_unidad_medida": unidad.ID_Unidad_de_medida,
        "nombre": unidad.Nombre,
        "abreviatura": unidad.Abreviatura,
        "activo": unidad.Activo,
        "productos_count": productos_count
    }

# Crear nueva unidad de medida
@router.post("/", response_model=UnidadMedidaCompleta)
async def create_unidad_medida(
    unidad: UnidadMedidaCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe una unidad con el mismo nombre o abreviatura
    existe = db.query(Unidades_de_medida).filter(
        (Unidades_de_medida.Nombre == unidad.nombre) |
        (Unidades_de_medida.Abreviatura == unidad.abreviatura)
    ).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una unidad de medida con este nombre o abreviatura"
        )
    
    # Crear nueva unidad
    db_unidad = Unidades_de_medida(
        Nombre=unidad.nombre,
        Abreviatura=unidad.abreviatura,
        Activo=unidad.activo
    )
    db.add(db_unidad)
    db.commit()
    db.refresh(db_unidad)
    
    return {
        "id_unidad_medida": db_unidad.ID_Unidad_de_medida,
        "nombre": db_unidad.Nombre,
        "abreviatura": db_unidad.Abreviatura,
        "activo": db_unidad.Activo,
        "productos_count": 0  # Nueva unidad, no tiene productos
    }

# Actualizar unidad de medida
@router.put("/{unidad_id}", response_model=UnidadMedidaCompleta)
async def update_unidad_medida(
    unidad: UnidadMedidaUpdate,
    unidad_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar unidad existente
    db_unidad = db.query(Unidades_de_medida).filter(
        Unidades_de_medida.ID_Unidad_de_medida == unidad_id
    ).first()
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    # Verificar nombre y abreviatura únicos
    if unidad.nombre or unidad.abreviatura:
        existe = db.query(Unidades_de_medida).filter(
            (Unidades_de_medida.ID_Unidad_de_medida != unidad_id) &
            ((Unidades_de_medida.Nombre == unidad.nombre) |
             (Unidades_de_medida.Abreviatura == unidad.abreviatura))
        ).first()
        if existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una unidad de medida con este nombre o abreviatura"
            )
    
    # Actualizar campos
    for key, value in unidad.dict(exclude_unset=True).items():
        setattr(db_unidad, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_unidad)
    
    # Obtener conteo de productos
    productos_count = db.query(func.count(Productos.ID_Producto)).filter(
        Productos.ID_Unidad_de_medida == unidad_id,
        Productos.Activo == True
    ).scalar()
    
    return {
        "id_unidad_medida": db_unidad.ID_Unidad_de_medida,
        "nombre": db_unidad.Nombre,
        "abreviatura": db_unidad.Abreviatura,
        "activo": db_unidad.Activo,
        "productos_count": productos_count
    }

# Eliminar unidad de medida (soft delete)
@router.delete("/{unidad_id}")
async def delete_unidad_medida(
    unidad_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar unidad
    db_unidad = db.query(Unidades_de_medida).filter(
        Unidades_de_medida.ID_Unidad_de_medida == unidad_id
    ).first()
    if not db_unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada")
    
    # Verificar si tiene productos asociados
    tiene_productos = db.query(func.count(Productos.ID_Producto)).filter(
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
