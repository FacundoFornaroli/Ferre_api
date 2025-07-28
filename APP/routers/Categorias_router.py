from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Categorias_schema import (
    CategoriaBase,
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaSimple,
    CategoriaCompleta,
    CategoriaList,
    CategoriaEstadisticas
)
from APP.DB.Categorias_model import Categorias
from sqlalchemy import func, and_
from APP.DB.Productos_model import Productos

router = APIRouter(
    prefix="/categorias",
    tags=["Categorias"]
)

# Obtener todas las categorías con paginación y filtros
@router.get("/", response_model=CategoriaList)
async def get_categorias(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    categoria_padre: Optional[int] = Query(None, description="Filtrar por categoría padre"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o descripción"),
    db: Session = Depends(get_db)
):
    # Query base con conteo de productos
    query = db.query(
        Categorias,
        func.count(Productos.ID_Producto).label('productos_count')
    ).outerjoin(
        Productos, and_(
            Productos.ID_Categoria == Categorias.ID_Categoria,
            Productos.Activo == True
        )
    ).group_by(
        Categorias.ID_Categoria,
        Categorias.Nombre,
        Categorias.Descripcion,
        Categorias.Categoria_Padre,
        Categorias.Activo,
        Categorias.Fecha_Creacion
    )
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Categorias.Activo == activo)
    if categoria_padre is not None:
        query = query.filter(Categorias.Categoria_Padre == categoria_padre)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Categorias.Nombre.ilike(search)) |
            (Categorias.Descripcion.ilike(search))
        )
    
    # Contar total de registros (necesitamos una subquery para el conteo total)
    total = db.query(func.count(Categorias.ID_Categoria)).scalar()
    
    # Aplicar paginación
    resultados = query.offset(skip).limit(limit).all()
    
    # Procesar resultados
    categorias_procesadas = []
    for categoria, productos_count in resultados:
        categoria_dict = {
            "id_categoria": categoria.ID_Categoria,
            "nombre": categoria.Nombre,
            "descripcion": categoria.Descripcion,
            "categoria_padre": categoria.Categoria_Padre,
            "activo": categoria.Activo,
            "productos_count": productos_count
        }
        categorias_procesadas.append(categoria_dict)
    
    return {
        "total_registros": total,
        "pagina_actual": skip // limit + 1,
        "total_paginas": (total + limit - 1) // limit,
        "categorias": categorias_procesadas
    }

# Obtener una categoría por ID
@router.get("/{categoria_id}", response_model=CategoriaCompleta)
async def get_categoria(
    categoria_id: int = Path(..., gt=0, description="ID de la categoría"),
    db: Session = Depends(get_db)
):
    # Query con conteo de productos
    result = db.query(
        Categorias,
        func.count(Productos.ID_Producto).label('productos_count')
    ).outerjoin(
        Productos, and_(
            Productos.ID_Categoria == Categorias.ID_Categoria,
            Productos.Activo == True
        )
    ).filter(
        Categorias.ID_Categoria == categoria_id
    ).group_by(
        Categorias.ID_Categoria,
        Categorias.Nombre,
        Categorias.Descripcion,
        Categorias.Categoria_Padre,
        Categorias.Activo,
        Categorias.Fecha_Creacion
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    categoria, productos_count = result
    
    # Obtener subcategorías
    subcategorias = db.query(
        Categorias,
        func.count(Productos.ID_Producto).label('productos_count')
    ).outerjoin(
        Productos, and_(
            Productos.ID_Categoria == Categorias.ID_Categoria,
            Productos.Activo == True
        )
    ).filter(
        Categorias.Categoria_Padre == categoria_id
    ).group_by(
        Categorias.ID_Categoria,
        Categorias.Nombre,
        Categorias.Descripcion,
        Categorias.Categoria_Padre,
        Categorias.Activo,
        Categorias.Fecha_Creacion
    ).all()
    
    # Procesar subcategorías
    subcategorias_procesadas = []
    for subcat, subcat_productos_count in subcategorias:
        subcat_dict = {
            "id_categoria": subcat.ID_Categoria,
            "nombre": subcat.Nombre,
            "descripcion": subcat.Descripcion,
            "categoria_padre": subcat.Categoria_Padre,
            "activo": subcat.Activo,
            "productos_count": subcat_productos_count
        }
        subcategorias_procesadas.append(subcat_dict)
    
    # Construir respuesta
    return {
        "id_categoria": categoria.ID_Categoria,
        "nombre": categoria.Nombre,
        "descripcion": categoria.Descripcion,
        "categoria_padre": categoria.Categoria_Padre,
        "activo": categoria.Activo,
        "fecha_creacion": categoria.Fecha_Creacion,
        "productos_count": productos_count,
        "subcategorias": subcategorias_procesadas
    }

# Crear nueva categoría
@router.post("/", response_model=CategoriaCompleta)
async def create_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe una categoría con el mismo nombre
    db_categoria = db.query(Categorias).filter(Categorias.Nombre == categoria.nombre).first()
    if db_categoria:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con este nombre")
    
    # Verificar categoría padre si se especifica
    if categoria.categoria_padre:
        padre = db.query(Categorias).filter(Categorias.ID_Categoria == categoria.categoria_padre).first()
        if not padre:
            raise HTTPException(status_code=404, detail="Categoría padre no encontrada")
    
    # Crear nueva categoría
    db_categoria = Categorias(
        Nombre=categoria.nombre,
        Descripcion=categoria.descripcion,
        Categoria_Padre=categoria.categoria_padre
    )
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Actualizar categoría
@router.put("/{categoria_id}", response_model=CategoriaCompleta)
async def update_categoria(
    categoria: CategoriaUpdate,
    categoria_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar categoría existente
    db_categoria = db.query(Categorias).filter(Categorias.ID_Categoria == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar nombre único si se está actualizando
    if categoria.nombre:
        nombre_existente = db.query(Categorias).filter(
            Categorias.Nombre == categoria.nombre,
            Categorias.ID_Categoria != categoria_id
        ).first()
        if nombre_existente:
            raise HTTPException(status_code=400, detail="Ya existe una categoría con este nombre")
    
    # Verificar categoría padre si se está actualizando
    if categoria.categoria_padre:
        if categoria.categoria_padre == categoria_id:
            raise HTTPException(status_code=400, detail="Una categoría no puede ser su propia padre")
        padre = db.query(Categorias).filter(Categorias.ID_Categoria == categoria.categoria_padre).first()
        if not padre:
            raise HTTPException(status_code=404, detail="Categoría padre no encontrada")
    
    # Actualizar campos
    for key, value in categoria.dict(exclude_unset=True).items():
        setattr(db_categoria, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Eliminar categoría (soft delete)
@router.delete("/{categoria_id}")
async def delete_categoria(
    categoria_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar categoría
    db_categoria = db.query(Categorias).filter(Categorias.ID_Categoria == categoria_id).first()
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar si tiene subcategorías
    tiene_subcategorias = db.query(Categorias).filter(Categorias.Categoria_Padre == categoria_id).first()
    if tiene_subcategorias:
        raise HTTPException(status_code=400, detail="No se puede eliminar una categoría que tiene subcategorías")
    
    # Verificar si tiene productos asociados
    tiene_productos = db.query(func.count()).select_from(Productos).filter(
        Productos.ID_Categoria == categoria_id
    ).scalar()
    if tiene_productos:
        # Soft delete
        db_categoria.Activo = False
        db.commit()
        return {"message": "Categoría desactivada porque tiene productos asociados"}
    else:
        # Hard delete si no tiene productos
        db.delete(db_categoria)
        db.commit()
        return {"message": "Categoría eliminada"}

# Obtener subcategorías
@router.get("/{categoria_id}/subcategorias", response_model=List[CategoriaSimple])
async def get_subcategorias(
    categoria_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    subcategorias = db.query(Categorias).filter(Categorias.Categoria_Padre == categoria_id).all()
    return subcategorias

# Obtener árbol de categorías
@router.get("/arbol", response_model=List[dict])
async def get_arbol_categorias(
    db: Session = Depends(get_db)
):
    def construir_arbol(categoria_padre=None):
        categorias = db.query(Categorias).filter(
            Categorias.Categoria_Padre == categoria_padre,
            Categorias.Activo == True
        ).all()
        
        return [
            {
                "id": cat.ID_Categoria,
                "nombre": cat.Nombre,
                "subcategorias": construir_arbol(cat.ID_Categoria)
            }
            for cat in categorias
        ]
    
    return construir_arbol()

# Obtener estadísticas de categorías
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_categorias(
    db: Session = Depends(get_db)
):
    total_categorias = db.query(func.count(Categorias.ID_Categoria)).scalar()
    categorias_activas = db.query(func.count(Categorias.ID_Categoria)).filter(Categorias.Activo == True).scalar()
    categorias_principales = db.query(func.count(Categorias.ID_Categoria)).filter(Categorias.Categoria_Padre == None).scalar()
    
    # Categorías con más productos
    categorias_productos = db.query(
        Categorias.ID_Categoria,
        Categorias.Nombre,
        func.count(Productos.ID_Producto).label('total_productos')
    ).join(Productos).group_by(Categorias.ID_Categoria).order_by(func.count(Productos.ID_Producto).desc()).limit(5).all()
    
    return {
        "total_categorias": total_categorias,
        "categorias_activas": categorias_activas,
        "categorias_principales": categorias_principales,
        "categorias_mas_productos": [
            {
                "id": cat.ID_Categoria,
                "nombre": cat.Nombre,
                "total_productos": cat.total_productos
            }
            for cat in categorias_productos
        ]
    }