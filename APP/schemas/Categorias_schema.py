from pydantic import BaseModel, Field, validator, constr
from typing import Optional, List
from datetime import datetime

# Schema Base: Define los campos comunes que se usan tanto para crear como para respuestas
class CategoriaBase(BaseModel):
    # constr permite definir restricciones para strings
    # strip_whitespace=True elimina espacios al inicio y final
    # min_length y max_length validan la longitud según la DB
    nombre: constr(strip_whitespace=True, min_length=2, max_length=100)
    
    # Optional porque no es obligatorio
    descripcion: Optional[str] = Field(
        None,  # valor por defecto
        max_length=500,  # máximo según DB
        description="Descripción detallada de la categoría"  # para documentación
    )
    
    # Optional porque puede no tener categoría padre
    categoria_padre: Optional[int] = Field(
        None,
        description="ID de la categoría padre si es una subcategoría"
    )

# Schema para Crear: Solo los campos necesarios para crear
class CategoriaCreate(CategoriaBase):
    # Hereda todos los campos de CategoriaBase
    
    @validator('categoria_padre')
    def validar_categoria_padre(cls, v, values):
        # Validación personalizada: una categoría no puede ser su propia padre
        if v == values.get('id_categoria'):
            raise ValueError('Una categoría no puede ser su propia padre')
        return v

# Schema para Actualizar: Todos los campos son opcionales
class CategoriaUpdate(BaseModel):
    nombre: Optional[constr(strip_whitespace=True, min_length=2, max_length=100)] = None
    descripcion: Optional[str] = Field(None, max_length=500)
    categoria_padre: Optional[int] = None
    activo: Optional[bool] = None

# Schema para Respuesta: Todos los campos que devuelve la API
class Categoria(CategoriaBase):
    id_categoria: int
    activo: bool
    fecha_creacion: datetime
    
    # Campos para relaciones
    subcategorias: List['Categoria'] = []  # Lista de subcategorías

    class Config:
        orm_mode = True  # Permite convertir modelos SQLAlchemy a Pydantic
        schema_extra = {
            "example": {
                "id_categoria": 1,
                "nombre": "Herramientas Eléctricas",
                "descripcion": "Todo tipo de herramientas eléctricas",
                "categoria_padre": None,
                "activo": True,
                "fecha_creacion": "2024-01-01T00:00:00",
                "subcategorias": [],
            }
        }

# Schema para respuesta en lista (sin algunos campos para reducir datos)
class CategoriaList(BaseModel):
    id_categoria: int
    nombre: str
    activo: bool

    class Config:
        orm_mode = True
