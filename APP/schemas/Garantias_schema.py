from pydantic import BaseModel, Field, validator, constr
from typing import Optional
from datetime import datetime

class GarantiaBase(BaseModel):
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    tiempo_garantia: int = Field(
        ...,
        description="Tiempo de garantía en días",
        example=365,
        gt=0  # greater than 0
    )
    tipo_garantia: constr(max_length=50) = Field(
        ...,
        description="Tipo de garantía",
        example="Fábrica"
    )
    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada de la garantía",
        example="Garantía oficial del fabricante por defectos de fabricación"
    )

    @validator('tipo_garantia')
    def validar_tipo_garantia(cls, v):
        tipos_validos = ['Fábrica', 'Local', 'Extendida']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de garantía debe ser uno de: {", ".join(tipos_validos)}')
        return v

    @validator('tiempo_garantia')
    def validar_tiempo_garantia(cls, v):
        if v <= 0:
            raise ValueError('El tiempo de garantía debe ser mayor a 0 días')
        if v > 3650:  # máximo 10 años
            raise ValueError('El tiempo de garantía no puede ser mayor a 10 años (3650 días)')
        return v

class GarantiaCreate(GarantiaBase):
    pass

class GarantiaUpdate(BaseModel):
    tiempo_garantia: Optional[int] = Field(None, gt=0)
    tipo_garantia: Optional[constr(max_length=50)] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

    @validator('tipo_garantia')
    def validar_tipo_garantia(cls, v):
        if v is not None:
            tipos_validos = ['Fábrica', 'Local', 'Extendida']
            if v not in tipos_validos:
                raise ValueError(f'Tipo de garantía debe ser uno de: {", ".join(tipos_validos)}')
        return v

    @validator('tiempo_garantia')
    def validar_tiempo_garantia(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError('El tiempo de garantía debe ser mayor a 0 días')
            if v > 3650:
                raise ValueError('El tiempo de garantía no puede ser mayor a 10 años (3650 días)')
        return v

class GarantiaSimple(GarantiaBase):
    id_garantia: int = Field(..., description="ID único de la garantía")
    activo: bool = Field(..., description="Estado de la garantía")

    class Config:
        orm_mode = True

class GarantiaCompleta(GarantiaSimple):
    producto_nombre: str = Field(
        ...,
        description="Nombre del producto",
        example="Martillo Profesional"
    )
    producto_codigo: Optional[str] = Field(
        None,
        description="Código o SKU del producto",
        example="MART-001"
    )
    producto_categoria: str = Field(
        ...,
        description="Categoría del producto",
        example="Herramientas"
    )
    fecha_vencimiento_ejemplo: str = Field(
        ...,
        description="Ejemplo de fecha de vencimiento para una compra hoy",
        example="2025-01-15"
    )
    garantias_activas: int = Field(
        0,
        description="Cantidad de garantías activas de este producto",
        example=5
    )
    garantias_ejecutadas: int = Field(
        0,
        description="Cantidad de garantías ejecutadas históricamente",
        example=2
    )
    tiempo_garantia_formateado: str = Field(
        ...,
        description="Tiempo de garantía en formato legible",
        example="1 año"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_garantia": 1,
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_categoria": "Herramientas",
                "tiempo_garantia": 365,
                "tiempo_garantia_formateado": "1 año",
                "tipo_garantia": "Fábrica",
                "descripcion": "Garantía oficial del fabricante por defectos de fabricación",
                "activo": True,
                "fecha_vencimiento_ejemplo": "2025-01-15",
                "garantias_activas": 5,
                "garantias_ejecutadas": 2
            }
        }

class GarantiaList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    garantias: list[GarantiaSimple]

    class Config:
        orm_mode = True

# Schema para registro de ejecución de garantía
class EjecucionGarantia(BaseModel):
    id_garantia: int
    id_factura_venta: int = Field(
        ...,
        description="ID de la factura de venta original",
        example=1
    )
    fecha_compra: datetime
    fecha_reclamo: datetime = Field(
        ...,
        description="Fecha del reclamo",
        example="2024-01-15T10:30:00"
    )
    motivo: str = Field(
        ...,
        description="Motivo del reclamo",
        example="Falla en el mecanismo de ajuste"
    )
    estado: str = Field(
        ...,
        description="Estado del reclamo",
        example="Pendiente"
    )
    resolucion: Optional[str] = Field(
        None,
        description="Resolución del reclamo",
        example="Se aprueba el cambio del producto"
    )

    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['Pendiente', 'En Revisión', 'Aprobada', 'Rechazada', 'Completada']
        if v not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_garantia": 1,
                "id_factura_venta": 1,
                "fecha_compra": "2023-01-15T10:30:00",
                "fecha_reclamo": "2024-01-15T10:30:00",
                "motivo": "Falla en el mecanismo de ajuste",
                "estado": "Pendiente",
                "resolucion": None
            }
        }

# Schema para estadísticas de garantías
class EstadisticasGarantias(BaseModel):
    total_garantias_activas: int
    garantias_por_tipo: dict = Field(
        ...,
        example={
            "Fábrica": 150,
            "Local": 75,
            "Extendida": 25
        }
    )
    garantias_ejecutadas_mes: int
    porcentaje_aprobacion: float
    tiempo_promedio_resolucion: float
    productos_mas_reclamados: list[dict]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "total_garantias_activas": 250,
                "garantias_por_tipo": {
                    "Fábrica": 150,
                    "Local": 75,
                    "Extendida": 25
                },
                "garantias_ejecutadas_mes": 15,
                "porcentaje_aprobacion": 85.5,
                "tiempo_promedio_resolucion": 3.5,
                "productos_mas_reclamados": [
                    {
                        "producto": "Martillo Profesional",
                        "reclamos": 5,
                        "porcentaje_aprobacion": 80.0
                    }
                ]
            }
        }
