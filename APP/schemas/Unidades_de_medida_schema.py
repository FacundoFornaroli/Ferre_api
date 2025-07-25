from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime

# Schema Base
class Unidad_de_medida_base(BaseModel):
    nombre: constr(min_length=2, max_length=50) = Field(
        ...,
        descripcion= "Nombre de la unidad de medida",
        example= "Kilogramo"
    )
    abreviatura: constr(min_length=2, max_length=10) = Field(
        ...,
        descripcion= "Abreviatura de la unidad de medida",
        example= "kg"
    )
    

class Unidad_de_medida_create(Unidad_de_medida_base):
    pass

# Schema para Actualizar
class Unidad_de_medida_update(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=50)] = None
    abreviatura: Optional[constr(min_length=2, max_length=10)] = None
    activo: Optional[bool] = None

# Schema para respuesta básica
class Unidad_de_medida_simple(Unidad_de_medida_base):
    id_unidad_de_medida: int = Field(
        ...;
        description= "ID unico de la unidad de medida"
        example= 1
    )
    activo: bool

    class Config:
        orm_mode = True

# Schema para respuesta completa
class Unidad_de_medida_completa(Unidad_de_medida_simple):
    fecha_creacion: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_unidad_de_medida": 1,
                "nombre": "Kilogramo",
                "abreviatura": "kg",
                "activo": True,
                "fecha_creacion": "2024-01-20T10:00:00"
            }
        }
    
