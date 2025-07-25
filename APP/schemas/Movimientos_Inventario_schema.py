from pydantic import BaseModel, Field, validator, condecimal, constr
from typing import Optional
from datetime import datetime

class MovimientoInventarioBase(BaseModel):
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
    tipo: constr(max_length=15) = Field(
        ...,
        description="Tipo de movimiento",
        example="Compra"
    )
    cantidad: int = Field(
        ...,
        description="Cantidad del movimiento",
        example=10
    )
    costo_unitario: Optional[condecimal(gt=0, decimal_places=2)] = Field(
        None,
        description="Costo unitario del producto",
        example=3500.00
    )
    id_referencia: Optional[int] = Field(
        None,
        description="ID de referencia (factura, OC, etc.)",
        example=1
    )
    tipo_referencia: Optional[constr(max_length=20)] = Field(
        None,
        description="Tipo de referencia",
        example="OC"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones del movimiento"
    )

    @validator('tipo')
    def validar_tipo_movimiento(cls, v):
        tipos_validos = ['Compra', 'Venta', 'Transferencia', 'Ajuste', 'Devolucion']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de movimiento debe ser uno de: {", ".join(tipos_validos)}')
        return v

    @validator('cantidad')
    def validar_cantidad(cls, v, values):
        if 'tipo' in values:
            # Para ventas y transferencias salientes, la cantidad debe ser negativa
            if values['tipo'] in ['Venta', 'Transferencia'] and v > 0:
                raise ValueError('La cantidad debe ser negativa para ventas y transferencias salientes')
            # Para compras y devoluciones, la cantidad debe ser positiva
            elif values['tipo'] in ['Compra', 'Devolucion'] and v < 0:
                raise ValueError('La cantidad debe ser positiva para compras y devoluciones')
        return v

    @validator('tipo_referencia')
    def validar_tipo_referencia(cls, v, values):
        if v:
            tipos_validos = ['Factura', 'OC', 'Transferencia', 'Devolucion']
            if v not in tipos_validos:
                raise ValueError(f'Tipo de referencia debe ser uno de: {", ".join(tipos_validos)}')
            # Validar que id_referencia exista si hay tipo_referencia
            if 'id_referencia' not in values or values['id_referencia'] is None:
                raise ValueError('Debe proporcionar un ID de referencia cuando especifica el tipo')
        return v

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioUpdate(BaseModel):
    observaciones: Optional[str] = None

class MovimientoInventarioSimple(MovimientoInventarioBase):
    id_movimiento: int = Field(..., description="ID único del movimiento")
    fecha: datetime
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario que registró el movimiento"
    )

    class Config:
        orm_mode = True

class MovimientoInventarioCompleto(MovimientoInventarioSimple):
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
    sucursal_nombre: str = Field(
        ...,
        description="Nombre de la sucursal",
        example="Sucursal Centro"
    )
    stock_anterior: int = Field(
        ...,
        description="Stock antes del movimiento",
        example=45
    )
    stock_actual: int = Field(
        ...,
        description="Stock después del movimiento",
        example=55
    )
    referencia_detalle: Optional[dict] = Field(
        None,
        description="Detalles de la referencia",
        example={
            "tipo": "OC",
            "numero": "OC-2024-00001",
            "fecha": "2024-01-15T10:30:00"
        }
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_movimiento": 1,
                "fecha": "2024-01-15T10:30:00",
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "id_sucursal": 1,
                "sucursal_nombre": "Sucursal Centro",
                "tipo": "Compra",
                "cantidad": 10,
                "costo_unitario": 3500.00,
                "stock_anterior": 45,
                "stock_actual": 55,
                "usuario_nombre": "María Elena Rodríguez",
                "id_referencia": 1,
                "tipo_referencia": "OC",
                "referencia_detalle": {
                    "tipo": "OC",
                    "numero": "OC-2024-00001",
                    "fecha": "2024-01-15T10:30:00"
                },
                "observaciones": "Ingreso por orden de compra"
            }
        }

class MovimientoInventarioList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    movimientos: list[MovimientoInventarioSimple]

    class Config:
        orm_mode = True

# Schema para análisis de movimientos
class AnalisisMovimientos(BaseModel):
    producto_id: int
    producto_nombre: str
    periodo: str = Field(..., example="2024-01")
    total_entradas: int
    total_salidas: int
    saldo_neto: int
    rotacion: float
    movimientos_por_tipo: dict = Field(
        ...,
        example={
            "Compra": {"cantidad": 50, "monto": 175000.00},
            "Venta": {"cantidad": -30, "monto": 135000.00},
            "Ajuste": {"cantidad": -2, "monto": 0}
        }
    )
    costo_promedio: condecimal(decimal_places=2)
    valor_stock: condecimal(decimal_places=2)

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "producto_id": 1,
                "producto_nombre": "Martillo Profesional",
                "periodo": "2024-01",
                "total_entradas": 50,
                "total_salidas": -32,
                "saldo_neto": 18,
                "rotacion": 0.64,
                "movimientos_por_tipo": {
                    "Compra": {"cantidad": 50, "monto": 175000.00},
                    "Venta": {"cantidad": -30, "monto": 135000.00},
                    "Ajuste": {"cantidad": -2, "monto": 0}
                },
                "costo_promedio": 3500.00,
                "valor_stock": 63000.00
            }
        }
