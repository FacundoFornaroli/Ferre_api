from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime

# Schema Base
class CategoriaBase(BaseModel):
    nombre: constr(min_length=2, max_length=100) = Field(
        ...,  # ... significa requerido
        description="Nombre de la categoría",
        example="Herramientas Eléctricas"
    )
    descripcion: Optional[str] = Field(
        None,
        max_length=500,
        description="Descripción detallada de la categoría",
        example="Todo tipo de herramientas eléctricas"
    )
    categoria_padre: Optional[int] = Field(
        None,
        description="ID de la categoría padre si es una subcategoría",
        example=1
    )

# Schema para Crear
class CategoriaCreate(CategoriaBase):
    pass

# Schema para Actualizar
class CategoriaUpdate(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=100)] = None
    descripcion: Optional[str] = None
    categoria_padre: Optional[int] = None
    activo: Optional[bool] = None

# Schema para respuesta básica (usado en listas)
class CategoriaSimple(CategoriaBase):
    id_categoria: int = Field(..., description="ID único de la categoría")
    activo: bool
    productos_count: int = Field(
        0,
        description="Cantidad de productos en esta categoría",
        example=5
    )

    class Config:
        from_attributes = True

# Schema para respuesta completa
class CategoriaCompleta(CategoriaSimple):
    fecha_creacion: datetime
    subcategorias: List['CategoriaSimple'] = []
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_categoria": 1,
                "nombre": "Herramientas Eléctricas",
                "descripcion": "Todo tipo de herramientas eléctricas",
                "categoria_padre": None,
                "activo": True,
                "productos_count": 5,
                "fecha_creacion": "2024-01-20T10:00:00",
                "subcategorias": []
            }
        }

# Schema para lista paginada de categorías
class CategoriaList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    categorias: List[CategoriaSimple]

# Schema para estadísticas
class CategoriaEstadisticas(BaseModel):
    total_categorias: int
    categorias_activas: int
    categorias_principales: int
    categorias_mas_productos: List[dict]

# Para evitar error de referencia circular con subcategorias
CategoriaSimple.update_forward_refs()
