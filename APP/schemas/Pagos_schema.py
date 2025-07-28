from pydantic import BaseModel, Field, validator, condecimal, constr
from typing import Optional, List
from datetime import datetime

class PagoBase(BaseModel):
    id_factura_venta: int = Field(
        ...,
        description="ID de la factura de venta",
        example=1
    )
    metodo: constr(max_length=30) = Field(
        ...,
        description="Método de pago",
        example="Efectivo"
    )
    monto: condecimal(gt=0, decimal_places=2) = Field(
        ...,
        description="Monto del pago",
        example=18150.00
    )
    numero_comprobante: Optional[constr(max_length=50)] = Field(
        None,
        description="Número de comprobante del pago",
        example="TRANS-123456"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones sobre el pago",
        example="Pago en efectivo sin cambio"
    )

    @validator('metodo')
    def validar_metodo_pago(cls, v):
        metodos_validos = ['Efectivo', 'Tarjeta', 'Transferencia', 'Cheque']
        if v not in metodos_validos:
            raise ValueError(f'Método de pago debe ser uno de: {", ".join(metodos_validos)}')
        return v

    @validator('numero_comprobante')
    def validar_comprobante_requerido(cls, v, values):
        if 'metodo' in values:
            # Si el pago es con tarjeta o transferencia, el comprobante es obligatorio
            if values['metodo'] in ['Tarjeta', 'Transferencia'] and not v:
                raise ValueError('Número de comprobante es requerido para pagos con tarjeta o transferencia')
        return v

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    metodo: Optional[constr(max_length=30)] = None
    monto: Optional[condecimal(gt=0, decimal_places=2)] = None
    numero_comprobante: Optional[constr(max_length=50)] = None
    observaciones: Optional[str] = None

    @validator('metodo')
    def validar_metodo_pago(cls, v):
        if v is not None:
            metodos_validos = ['Efectivo', 'Tarjeta', 'Transferencia', 'Cheque']
            if v not in metodos_validos:
                raise ValueError(f'Método de pago debe ser uno de: {", ".join(metodos_validos)}')
        return v

class PagoSimple(PagoBase):
    id_pago: int = Field(..., description="ID único del pago")
    fecha: datetime = Field(
        ...,
        description="Fecha y hora del pago",
        example="2024-01-15T10:30:00"
    )
    usuario_nombre: str = Field(
        ...,
        description="Nombre del usuario que registró el pago",
        example="María Elena Rodríguez"
    )

    class Config:
        from_attributes = True

class PagoCompleto(PagoSimple):
    factura_numero: str = Field(
        ...,
        description="Número de la factura",
        example="A-0001-00000001"
    )
    factura_total: condecimal(decimal_places=2) = Field(
        ...,
        description="Monto total de la factura",
        example=18150.00
    )
    factura_saldo_restante: condecimal(decimal_places=2) = Field(
        ...,
        description="Saldo restante de la factura después de este pago",
        example=0.00
    )
    cliente_nombre: str = Field(
        ...,
        description="Nombre del cliente",
        example="Juan Carlos González"
    )
    sucursal_nombre: str = Field(
        ...,
        description="Nombre de la sucursal",
        example="Sucursal Centro"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_pago": 1,
                "id_factura_venta": 1,
                "factura_numero": "A-0001-00000001",
                "factura_total": 18150.00,
                "factura_saldo_restante": 0.00,
                "metodo": "Efectivo",
                "monto": 18150.00,
                "numero_comprobante": None,
                "fecha": "2024-01-15T10:30:00",
                "usuario_nombre": "María Elena Rodríguez",
                "cliente_nombre": "Juan Carlos González",
                "sucursal_nombre": "Sucursal Centro",
                "observaciones": "Pago en efectivo sin cambio"
            }
        }

class PagoList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    pagos: List[PagoSimple]

    class Config:
        from_attributes = True

# Schema adicional para resumen de pagos por método
class ResumenPagosPorMetodo(BaseModel):
    metodo: str
    cantidad_pagos: int
    monto_total: condecimal(decimal_places=2)
    porcentaje_del_total: float

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "metodo": "Efectivo",
                "cantidad_pagos": 150,
                "monto_total": 275000.00,
                "porcentaje_del_total": 65.5
            }
        }
