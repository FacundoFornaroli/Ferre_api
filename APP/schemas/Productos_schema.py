from pydantic import BaseModel, Field, constr, validator, condecimal
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

# Schema Base
class ProductoBase(BaseModel):
    nombre: constr(min_length=3, max_length=150, strip_whitespace=True) = Field(
        ...,
        description="Nombre del producto",
        example="Martillo Profesional"
    )
    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada del producto",
        example="Martillo profesional de acero forjado con mango ergonómico"
    )
    codigo_barras: Optional[constr(max_length=50, strip_whitespace=True)] = Field(
        None,
        description="Código de barras del producto",
        example="7790001234567"
    )
    sku: Optional[constr(max_length=20, strip_whitespace=True)] = Field(
        None,
        description="Código SKU del producto",
        example="MART-001"
    )
    marca: Optional[constr(max_length=100)] = Field(
        None,
        description="Marca del producto",
        example="Stanley"
    )
    modelo: Optional[constr(max_length=100)] = Field(
        None,
        description="Modelo del producto",
        example="STHT51456"
    )
    precio: condecimal(gt=0, decimal_places=2) = Field(
        ...,
        description="Precio de venta al público",
        example=2500.00
    )
    costo: condecimal(gt=0, decimal_places=2) = Field(
        ...,
        description="Costo de adquisición",
        example=1500.00
    )
    precio_mayorista: Optional[condecimal(gt=0, decimal_places=2)] = Field(
        None,
        description="Precio para ventas mayoristas",
        example=2000.00
    )
    id_categoria: int = Field(
        ...,
        description="ID de la categoría del producto",
        example=1
    )
    id_unidad_de_medida: int = Field(
        ...,
        description="ID de la unidad de medida",
        example=1
    )
    peso: Optional[condecimal(ge=0, decimal_places=2)] = Field(
        None,
        description="Peso en kilogramos",
        example=0.5
    )
    dimensiones: Optional[constr(max_length=50)] = Field(
        None,
        description="Dimensiones en formato LxAxH",
        example="30x10x5"
    )

    @validator('precio_mayorista')
    def validar_precio_mayorista(cls, v, values):
        if v is not None:
            if 'precio' in values and v >= values['precio']:
                raise ValueError('El precio mayorista debe ser menor al precio de venta')
            if 'costo' in values and v <= values['costo']:
                raise ValueError('El precio mayorista debe ser mayor al costo')
        return v

    @validator('precio')
    def validar_precio(cls, v, values):
        if 'costo' in values and v <= values['costo']:
            raise ValueError('El precio debe ser mayor al costo')
        return v

    @validator('dimensiones')
    def validar_dimensiones(cls, v):
        if v:
            parts = v.split('x')
            if len(parts) != 3 or not all(p.replace('.','').isdigit() for p in parts):
                raise ValueError('Dimensiones deben estar en formato LxAxH (ejemplo: 30x10x5)')
        return v

# Schema para Crear
class ProductoCreate(ProductoBase):
    pass

# Schema para Actualizar
class ProductoUpdate(BaseModel):
    nombre: Optional[constr(min_length=3, max_length=150)] = None
    descripcion: Optional[str] = None
    codigo_barras: Optional[constr(max_length=50)] = None
    sku: Optional[constr(max_length=20)] = None
    marca: Optional[constr(max_length=100)] = None
    modelo: Optional[constr(max_length=100)] = None
    precio: Optional[condecimal(gt=0, decimal_places=2)] = None
    costo: Optional[condecimal(gt=0, decimal_places=2)] = None
    precio_mayorista: Optional[condecimal(gt=0, decimal_places=2)] = None
    id_categoria: Optional[int] = None
    id_unidad_de_medida: Optional[int] = None
    peso: Optional[condecimal(ge=0, decimal_places=2)] = None
    dimensiones: Optional[constr(max_length=50)] = None
    activo: Optional[bool] = None

# Schema para respuesta básica
class ProductoSimple(ProductoBase):
    id_producto: int = Field(..., description="ID único del producto")
    activo: bool
    stock_total: int = Field(
        0,
        description="Stock total en todas las sucursales",
        example=100
    )

    class Config:
        orm_mode = True

# Schema para respuesta completa
class ProductoCompleta(ProductoSimple):
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    categoria: str = Field(..., description="Nombre de la categoría")
    unidad_medida: str = Field(..., description="Nombre de la unidad de medida")
    stock_por_sucursal: List[dict] = Field(
        [],
        description="Stock disponible por sucursal",
        example=[{"sucursal": "Centro", "stock": 50}, {"sucursal": "Norte", "stock": 50}]
    )
    tiene_garantia: bool = Field(
        False,
        description="Indica si el producto tiene garantía"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_producto": 1,
                "nombre": "Martillo Profesional",
                "descripcion": "Martillo profesional de acero forjado",
                "codigo_barras": "7790001234567",
                "sku": "MART-001",
                "marca": "Stanley",
                "modelo": "STHT51456",
                "precio": 2500.00,
                "costo": 1500.00,
                "precio_mayorista": 2000.00,
                "id_categoria": 1,
                "categoria": "Herramientas Manuales",
                "id_unidad_de_medida": 1,
                "unidad_medida": "Unidad",
                "peso": 0.5,
                "dimensiones": "30x10x5",
                "activo": True,
                "stock_total": 100,
                "stock_por_sucursal": [
                    {"sucursal": "Centro", "stock": 50},
                    {"sucursal": "Norte", "stock": 50}
                ],
                "tiene_garantia": True,
                "fecha_creacion": "2024-01-01T10:00:00",
                "fecha_actualizacion": "2024-01-20T15:30:00"
            }
        }
