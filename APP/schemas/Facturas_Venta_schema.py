from pydantic import BaseModel, Field, constr, validator, condecimal
from typing import Optional, List
from datetime import datetime

# Schema Base para Detalles de Factura
class DetalleFacturaBase(BaseModel):
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
        description="Precio unitario",
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
            raise ValueError('El descuento no puede ser mayor o igual al precio')
        return v

# Schema Base para Factura
class FacturaVentaBase(BaseModel):
    id_cliente: int = Field(
        ...,
        description="ID del cliente",
        example=1
    )
    id_sucursal: int = Field(
        ...,
        description="ID de la sucursal",
        example=1
    )
    tipo_factura: constr(max_length=1) = Field(
        ...,
        description="Tipo de factura (A, B, C)",
        example="A"
    )
    condicion_iva: Optional[constr(max_length=50)] = Field(
        None,
        description="Condición IVA",
        example="IVA Responsable Inscripto"
    )
    forma_pago: Optional[constr(max_length=50)] = Field(
        None,
        description="Forma de pago",
        example="Efectivo"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones generales"
    )

    @validator('tipo_factura')
    def validar_tipo_factura(cls, v):
        if v not in ['A', 'B', 'C']:
            raise ValueError('Tipo de factura debe ser A, B o C')
        return v

# Schema para Crear Factura
class FacturaVentaCreate(FacturaVentaBase):
    detalles: List[DetalleFacturaBase]

# Schema para Actualizar Factura
class FacturaVentaUpdate(BaseModel):
    tipo_factura: Optional[constr(max_length=1)] = None
    condicion_iva: Optional[str] = None
    forma_pago: Optional[str] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['Emitida', 'Pagada', 'Anulada', 'Pendiente']
        if v and v not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v

# Schema para respuesta básica
class FacturaVentaSimple(BaseModel):
    id_factura_venta: int = Field(..., description="ID único de la factura")
    numero_factura: Optional[str] = Field(None, description="Número de factura")
    fecha: datetime
    tipo_factura: str
    estado: str
    total: condecimal(gt=0, decimal_places=2)
    cliente_nombre: str = Field(..., description="Nombre del cliente")
    sucursal_nombre: str = Field(..., description="Nombre de la sucursal")

    class Config:
        orm_mode = True

# Schema para Detalle en respuesta
class DetalleFacturaResponse(DetalleFacturaBase):
    id_detalle: int
    subtotal: condecimal(decimal_places=2)
    producto_nombre: str
    producto_codigo: str

    class Config:
        orm_mode = True

# Schema para respuesta completa
class FacturaVentaCompleta(FacturaVentaSimple):
    subtotal: condecimal(decimal_places=2)
    iva: condecimal(decimal_places=2)
    descuento: condecimal(decimal_places=2)
    usuario_nombre: str
    detalles: List[DetalleFacturaResponse]
    pagos_realizados: List[dict] = Field(
        [],
        description="Lista de pagos realizados",
        example=[
            {"fecha": "2024-01-15T10:30:00", "metodo": "Efectivo", "monto": 18150.00}
        ]
    )
    saldo_pendiente: condecimal(decimal_places=2) = Field(
        0,
        description="Saldo pendiente de pago",
        example=0.00
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_factura_venta": 1,
                "numero_factura": "A-0001-00000001",
                "fecha": "2024-01-15T10:30:00",
                "tipo_factura": "A",
                "estado": "Pagada",
                "cliente_nombre": "Juan Carlos González",
                "sucursal_nombre": "Sucursal Centro",
                "subtotal": 15000.00,
                "iva": 3150.00,
                "descuento": 0.00,
                "total": 18150.00,
                "usuario_nombre": "María Elena Rodríguez",
                "detalles": [
                    {
                        "id_detalle": 1,
                        "id_producto": 1,
                        "producto_nombre": "Martillo Profesional",
                        "producto_codigo": "MART-001",
                        "cantidad": 2,
                        "precio_unitario": 4500.00,
                        "descuento_unitario": 0.00,
                        "subtotal": 9000.00
                    }
                ],
                "pagos_realizados": [
                    {
                        "fecha": "2024-01-15T10:30:00",
                        "metodo": "Efectivo",
                        "monto": 18150.00
                    }
                ],
                "saldo_pendiente": 0.00,
                "observaciones": "Factura pagada en efectivo"
            }
        }

# Schema para respuesta de lista de facturas
class FacturaVentaList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    facturas: List[FacturaVentaSimple]

    class Config:
        orm_mode = True
