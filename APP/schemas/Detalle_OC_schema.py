from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime

class DetalleOCBase(BaseModel):
    id_oc: int = Field(
        ...,
        description="ID de la orden de compra",
        example=1
    )
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    cantidad: int = Field(
        ...,
        description="Cantidad del producto",
        example=10,
        gt=0  # greater than 0
    )
    costo_unitario: condecimal(gt=0, decimal_places=2) = Field(
        ...,
        description="Costo unitario del producto",
        example=3500.00
    )
    descuento_unitario: condecimal(ge=0, decimal_places=2) = Field(
        0,
        description="Descuento por unidad",
        example=0.00
    )

    @validator('descuento_unitario')
    def validar_descuento(cls, v, values):
        if 'costo_unitario' in values and v >= values['costo_unitario']:
            raise ValueError('El descuento no puede ser mayor o igual al costo unitario')
        return v

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleOCCreate(DetalleOCBase):
    pass

class DetalleOCUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    costo_unitario: Optional[condecimal(gt=0, decimal_places=2)] = None
    descuento_unitario: Optional[condecimal(ge=0, decimal_places=2)] = None

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v is not None and v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleOCSimple(DetalleOCBase):
    id_detalle_oc: int = Field(..., description="ID único del detalle")
    subtotal: condecimal(decimal_places=2) = Field(
        ...,
        description="Subtotal del detalle (cantidad * (costo_unitario - descuento_unitario))",
        example=35000.00
    )

    class Config:
        orm_mode = True

class DetalleOCCompleto(DetalleOCSimple):
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
    unidad_medida: str = Field(
        ...,
        description="Unidad de medida del producto",
        example="Unidad"
    )
    costo_anterior: Optional[condecimal(decimal_places=2)] = Field(
        None,
        description="Último costo registrado del producto",
        example=3200.00
    )
    variacion_costo: Optional[float] = Field(
        None,
        description="Variación porcentual respecto al último costo",
        example=9.375
    )
    stock_actual: int = Field(
        ...,
        description="Stock actual del producto en la sucursal",
        example=45
    )
    stock_pendiente_recibir: int = Field(
        0,
        description="Cantidad pendiente de recibir de otras órdenes",
        example=20
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_detalle_oc": 1,
                "id_oc": 1,
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_categoria": "Herramientas",
                "unidad_medida": "Unidad",
                "cantidad": 10,
                "costo_unitario": 3500.00,
                "descuento_unitario": 0.00,
                "subtotal": 35000.00,
                "costo_anterior": 3200.00,
                "variacion_costo": 9.375,
                "stock_actual": 45,
                "stock_pendiente_recibir": 20
            }
        }

class DetalleOCList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    detalles: list[DetalleOCSimple]

    class Config:
        orm_mode = True

# Schema adicional para análisis de costos
class AnalisisCostos(BaseModel):
    producto_id: int
    producto_nombre: str
    historial_costos: list[dict] = Field(
        ...,
        description="Historial de costos del producto",
        example=[
            {
                "fecha": "2024-01-15",
                "costo": 3500.00,
                "proveedor": "Ferretería Mayorista SA",
                "cantidad": 10
            },
            {
                "fecha": "2023-12-15",
                "costo": 3200.00,
                "proveedor": "Distribuidora del Sur",
                "cantidad": 15
            }
        ]
    )
    costo_promedio: condecimal(decimal_places=2)
    variacion_porcentual: float
    tendencia: str = Field(
        ...,
        description="Tendencia del costo",
        example="Ascendente"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "producto_id": 1,
                "producto_nombre": "Martillo Profesional",
                "historial_costos": [
                    {
                        "fecha": "2024-01-15",
                        "costo": 3500.00,
                        "proveedor": "Ferretería Mayorista SA",
                        "cantidad": 10
                    },
                    {
                        "fecha": "2023-12-15",
                        "costo": 3200.00,
                        "proveedor": "Distribuidora del Sur",
                        "cantidad": 15
                    }
                ],
                "costo_promedio": 3350.00,
                "variacion_porcentual": 9.375,
                "tendencia": "Ascendente"
            }
        }
