from pydantic import BaseModel, Field, constr, validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Schema Base
class Unidad_de_medida_base(BaseModel):
    nombre: constr(min_length=2, max_length=50, strip_whitespace=True) = Field(
        ...,
        description="Nombre de la unidad de medida",
        example="Kilogramo"
    )
    abreviatura: constr(min_length=1, max_length=10, strip_whitespace=True) = Field(
        ...,
        description="Abreviatura de la unidad de medida",
        example="kg"
    )

    # Validador para asegurar que nombre y abreviatura sean diferentes
    @validator('abreviatura')
    def validar_nombre_abreviatura(cls, v, values):
        if 'nombre' in values and v == values['nombre']:
            raise ValueError('La abreviatura no puede ser igual al nombre')
        return v

    @validator('nombre')
    def validar_nombre(cls, v):
        if v.lower() in ['none', 'null', 'undefined']:
            raise ValueError('Nombre no válido')
        return v.title()  # Capitaliza primera letra

    @validator('abreviatura')
    def validar_abreviatura(cls, v):
        if not v.isalnum():  # Solo letras y números
            raise ValueError('La abreviatura solo puede contener letras y números')
        return v.lower()  # Convierte a minúsculas


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
        ...,
        description="ID único de la unidad de medida",
        example=1
    )
    activo: bool
   

    class Config:
        orm_mode = True

# Schema para respuesta completa
class Unidad_de_medida_completa(Unidad_de_medida_simple):
    fecha_creacion: datetime
    # Eliminar la línea de productos si no es necesaria

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_unidad_de_medida": 1,
                "nombre": "Kilogramo",
                "abreviatura": "kg",
                "activo": True,
                "fecha_creacion": "2024-01-20T10:00:00",
                "productos_count": 5
            },
            "examples": [
                {
                    "nombre": "Metro",
                    "abreviatura": "m"
                },
                {
                    "nombre": "Litro",
                    "abreviatura": "l"
                },
                {
                    "nombre": "Unidad",
                    "abreviatura": "u"
                }
            ]
        }
    
