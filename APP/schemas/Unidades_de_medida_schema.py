from pydantic import BaseModel, Field, constr
from typing import Optional, List

class UnidadMedidaBase(BaseModel):
    nombre: constr(min_length=1, max_length=50) = Field(..., description="Nombre de la unidad de medida")
    abreviatura: constr(min_length=1, max_length=10) = Field(..., description="Abreviatura de la unidad de medida")
    activo: bool = Field(True, description="Estado de la unidad de medida")

    class Config:
        from_attributes = True

class UnidadMedidaCreate(UnidadMedidaBase):
    pass

class UnidadMedidaUpdate(BaseModel):
    nombre: Optional[constr(min_length=1, max_length=50)] = Field(None, description="Nombre de la unidad de medida")
    abreviatura: Optional[constr(min_length=1, max_length=10)] = Field(None, description="Abreviatura de la unidad de medida")
    activo: Optional[bool] = Field(None, description="Estado de la unidad de medida")

    class Config:
        from_attributes = True

class UnidadMedidaSimple(BaseModel):
    id_unidad_medida: int = Field(..., description="ID único de la unidad de medida")
    nombre: str = Field(..., description="Nombre de la unidad de medida")
    abreviatura: str = Field(..., description="Abreviatura de la unidad de medida")
    activo: bool = Field(..., description="Estado de la unidad de medida")
    productos_count: Optional[int] = Field(0, description="Cantidad de productos que usan esta unidad")

    class Config:
        from_attributes = True

class UnidadMedidaCompleta(UnidadMedidaSimple):
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_unidad_medida": 1,
                "nombre": "Kilogramo",
                "abreviatura": "kg",
                "activo": True,
                "productos_count": 10
            }
        }

class UnidadMedidaList(BaseModel):
    total_registros: int = Field(..., description="Total de registros encontrados")
    pagina_actual: int = Field(..., description="Número de página actual")
    total_paginas: int = Field(..., description="Total de páginas disponibles")
    unidades: List[UnidadMedidaSimple] = Field(..., description="Lista de unidades de medida")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_registros": 100,
                "pagina_actual": 1,
                "total_paginas": 10,
                "unidades": [
                    {
                        "id_unidad_medida": 1,
                        "nombre": "Kilogramo",
                        "abreviatura": "kg",
                        "activo": True,
                        "productos_count": 10
                    }
                ]
            }
        }
    
