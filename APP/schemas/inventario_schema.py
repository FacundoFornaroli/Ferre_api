from pydantic import BaseModel, Field, constr, validator
from typing import Optional
from datetime import datetime

# Schema Base
class InventarioBase(BaseModel):
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    id_sucursal: int = Field(
        ...,
        description="ID de la sucursal",
        example=1
    )
    stock_actual: int = Field(
        0,
        description="Stock actual del producto",
        example=50,
        ge=0  # greater or equal than 0
    )
    stock_minimo: int = Field(
        0,
        description="Stock mínimo del producto",
        example=10,
        ge=0
    )
    stock_maximo: int = Field(
        0,
        description="Stock máximo del producto",
        example=100,
        ge=0
    )
    ubicacion: Optional[constr(max_length=100)] = Field(
        None,
        description="Ubicación física en la sucursal",
        example="Pasillo A - Estante 1"
    )

    @validator('stock_maximo')
    def validar_stock_maximo(cls, v, values):
        if 'stock_minimo' in values and v < values['stock_minimo']:
            raise ValueError('El stock máximo debe ser mayor o igual al stock mínimo')
        return v

# Schema para Crear
class InventarioCreate(InventarioBase):
    pass

# Schema para Actualizar
class InventarioUpdate(BaseModel):
    stock_actual: Optional[int] = Field(None, ge=0)
    stock_minimo: Optional[int] = Field(None, ge=0)
    stock_maximo: Optional[int] = Field(None, ge=0)
    ubicacion: Optional[str] = None
    activo: Optional[bool] = None

# Schema para respuesta básica
class InventarioSimple(InventarioBase):
    id_inventario: int = Field(..., description="ID único del registro de inventario")
    activo: bool
    fecha_ultimo_movimiento: Optional[datetime] = Field(
        None,
        description="Fecha del último movimiento",
        example="2024-01-20T15:30:00"
    )
    estado_stock: str = Field(
        "Normal",
        description="Estado del stock",
        example="Normal"
    )

    class Config:
        orm_mode = True

# Schema para respuesta completa
class InventarioCompleta(InventarioSimple):
    producto_nombre: str = Field(
        ...,
        description="Nombre del producto",
        example="Martillo Profesional"
    )
    producto_codigo: str = Field(
        ...,
        description="Código del producto",
        example="MART-001"
    )
    sucursal_nombre: str = Field(
        ...,
        description="Nombre de la sucursal",
        example="Sucursal Centro"
    )
    movimientos_count: int = Field(
        0,
        description="Cantidad de movimientos en el último mes",
        example=15
    )
    rotacion_mensual: float = Field(
        0.0,
        description="Promedio de unidades movidas por mes",
        example=25.5
    )
    valor_stock: float = Field(
        0.0,
        description="Valor total del stock actual",
        example=25000.00
    )
    dias_sin_movimiento: Optional[int] = Field(
        None,
        description="Días desde el último movimiento",
        example=5
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_inventario": 1,
                "id_producto": 1,
                "id_sucursal": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "sucursal_nombre": "Sucursal Centro",
                "stock_actual": 50,
                "stock_minimo": 10,
                "stock_maximo": 100,
                "ubicacion": "Pasillo A - Estante 1",
                "activo": True,
                "fecha_ultimo_movimiento": "2024-01-20T15:30:00",
                "estado_stock": "Normal",
                "movimientos_count": 15,
                "rotacion_mensual": 25.5,
                "valor_stock": 25000.00,
                "dias_sin_movimiento": 5
            }
        }
