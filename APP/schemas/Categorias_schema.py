from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime

class CategoriaBase(BaseModel):
    nombre: constr(min_length=1, max_length=100) = Field(..., description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    categoria_padre: Optional[int] = Field(None, description="ID de la categoría padre")
    activo: bool = Field(True, description="Estado de la categoría")

    class Config:
        from_attributes = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    categoria_padre: Optional[int] = Field(None, description="ID de la categoría padre")
    activo: Optional[bool] = Field(None, description="Estado de la categoría")

    class Config:
        from_attributes = True

class CategoriaSimple(BaseModel):
    id_categoria: int = Field(..., description="ID único de la categoría")
    nombre: str = Field(..., description="Nombre de la categoría")
    descripcion: Optional[str] = Field(None, description="Descripción de la categoría")
    categoria_padre: Optional[int] = Field(None, description="ID de la categoría padre")
    activo: bool = Field(..., description="Estado de la categoría")
    productos_count: Optional[int] = Field(0, description="Cantidad de productos en la categoría")

    class Config:
        from_attributes = True

class CategoriaCompleta(CategoriaSimple):
    fecha_creacion: datetime = Field(..., description="Fecha de creación de la categoría")
    subcategorias: List[CategoriaSimple] = Field(default_factory=list, description="Lista de subcategorías")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_categoria": 1,
                "nombre": "Herramientas",
                "descripcion": "Categoría de herramientas",
                "categoria_padre": None,
                "activo": True,
                "fecha_creacion": "2024-01-01T00:00:00",
                "productos_count": 10,
                "subcategorias": []
            }
        }

class CategoriaList(BaseModel):
    total_registros: int = Field(..., description="Total de registros encontrados")
    pagina_actual: int = Field(..., description="Número de página actual")
    total_paginas: int = Field(..., description="Total de páginas disponibles")
    categorias: List[CategoriaSimple] = Field(..., description="Lista de categorías")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_registros": 100,
                "pagina_actual": 1,
                "total_paginas": 10,
                "categorias": [
                    {
                        "id_categoria": 1,
                        "nombre": "Herramientas",
                        "descripcion": "Categoría de herramientas",
                        "categoria_padre": None,
                        "activo": True,
                        "productos_count": 10
                    }
                ]
            }
        }

class CategoriaEstadisticas(BaseModel):
    total_categorias: int = Field(..., description="Total de categorías")
    categorias_activas: int = Field(..., description="Total de categorías activas")
    categorias_principales: int = Field(..., description="Total de categorías principales (sin padre)")
    categorias_mas_productos: List[dict] = Field(..., description="Top 5 categorías con más productos")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_categorias": 100,
                "categorias_activas": 95,
                "categorias_principales": 10,
                "categorias_mas_productos": [
                    {
                        "id": 1,
                        "nombre": "Herramientas",
                        "total_productos": 50
                    }
                ]
            }
        }
