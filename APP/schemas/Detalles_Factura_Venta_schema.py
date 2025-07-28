from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional, List
from datetime import datetime

class DetalleFacturaVentaBase(BaseModel):
    id_factura_venta: int = Field(
        ...,
        description="ID de la factura de venta",
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
        example=2,
        gt=0  # greater than 0
    )
    precio_unitario: condecimal(gt=0, decimal_places=2) = Field(
        ...,
        description="Precio unitario del producto",
        example=4500.00
    )
    descuento_unitario: condecimal(ge=0, decimal_places=2) = Field(
        0,
        description="Descuento por unidad",
        example=0.00
    )

    @validator('descuento_unitario')
    def validar_descuento(cls, v, values):
        if 'precio_unitario' in values and v >= values['precio_unitario']:
            raise ValueError('El descuento no puede ser mayor o igual al precio unitario')
        return v

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleFacturaVentaCreate(DetalleFacturaVentaBase):
    pass

class DetalleFacturaVentaUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    precio_unitario: Optional[condecimal(gt=0, decimal_places=2)] = None
    descuento_unitario: Optional[condecimal(ge=0, decimal_places=2)] = None

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v is not None and v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleFacturaVentaSimple(DetalleFacturaVentaBase):
    id_detalle: int = Field(..., description="ID único del detalle")
    subtotal: condecimal(decimal_places=2) = Field(
        ...,
        description="Subtotal del detalle (cantidad * (precio_unitario - descuento_unitario))",
        example=9000.00
    )

    class Config:
        from_attributes = True

class DetalleFacturaVentaCompleta(DetalleFacturaVentaSimple):
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
    stock_actual: int = Field(
        ...,
        description="Stock actual del producto en la sucursal",
        example=48
    )
    tiene_garantia: bool = Field(
        False,
        description="Indica si el producto tiene garantía",
        example=True
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_detalle": 1,
                "id_factura_venta": 1,
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_categoria": "Herramientas",
                "unidad_medida": "Unidad",
                "cantidad": 2,
                "precio_unitario": 4500.00,
                "descuento_unitario": 0.00,
                "subtotal": 9000.00,
                "stock_actual": 48,
                "tiene_garantia": True
            }
        }

class DetalleFacturaVentaList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    detalles: List[DetalleFacturaVentaSimple]

    class Config:
        from_attributes = True
