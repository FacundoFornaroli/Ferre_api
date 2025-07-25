from pydantic import BaseModel, Field, validator, condecimal, constr
from typing import Optional, List
from datetime import datetime, date

# Schema Base para Detalles de OC
class DetalleOCBase(BaseModel):
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

# Schema Base para Orden de Compra
class OrdenCompraBase(BaseModel):
    id_proveedor: int = Field(
        ...,
        description="ID del proveedor",
        example=1
    )
    id_sucursal: int = Field(
        ...,
        description="ID de la sucursal",
        example=1
    )
    fecha_entrega_esperada: Optional[date] = Field(
        None,
        description="Fecha esperada de entrega",
        example="2024-02-01"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones generales"
    )

    @validator('fecha_entrega_esperada')
    def validar_fecha_entrega(cls, v):
        if v and v < date.today():
            raise ValueError('La fecha de entrega esperada no puede ser anterior a hoy')
        return v

# Schema para Crear Orden de Compra
class OrdenCompraCreate(OrdenCompraBase):
    detalles: List[DetalleOCBase]

# Schema para Actualizar Orden de Compra
class OrdenCompraUpdate(BaseModel):
    fecha_entrega_esperada: Optional[date] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

    @validator('estado')
    def validar_estado(cls, v):
        estados_validos = ['Pendiente', 'Aprobada', 'Recibida', 'Cancelada']
        if v and v not in estados_validos:
            raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v

    @validator('fecha_entrega_esperada')
    def validar_fecha_entrega(cls, v):
        if v and v < date.today():
            raise ValueError('La fecha de entrega esperada no puede ser anterior a hoy')
        return v

# Schema para respuesta básica
class OrdenCompraSimple(BaseModel):
    id_oc: int = Field(..., description="ID único de la orden de compra")
    numero_oc: Optional[str] = Field(None, description="Número de orden de compra")
    fecha: datetime
    fecha_entrega_esperada: Optional[date]
    estado: str
    total: condecimal(gt=0, decimal_places=2)
    proveedor_nombre: str = Field(..., description="Nombre del proveedor")
    sucursal_nombre: str = Field(..., description="Nombre de la sucursal")

    class Config:
        orm_mode = True

# Schema para Detalle en respuesta
class DetalleOCResponse(DetalleOCBase):
    id_detalle_oc: int
    subtotal: condecimal(decimal_places=2)
    producto_nombre: str
    producto_codigo: str
    unidad_medida: str

    class Config:
        orm_mode = True

# Schema para respuesta completa
class OrdenCompraCompleta(OrdenCompraSimple):
    subtotal: condecimal(decimal_places=2)
    iva: condecimal(decimal_places=2)
    descuento: condecimal(decimal_places=2)
    usuario_nombre: str
    detalles: List[DetalleOCResponse]
    proveedor_info: dict = Field(
        ...,
        description="Información adicional del proveedor",
        example={
            "cuit": "30-12345678-9",
            "contacto": "Juan Pérez",
            "telefono": "11-1234-5678",
            "email": "juan@proveedor.com"
        }
    )
    dias_transcurridos: Optional[int] = Field(
        None,
        description="Días transcurridos desde la emisión",
        example=5
    )
    tiempo_entrega_estimado: Optional[int] = Field(
        None,
        description="Tiempo de entrega estimado en días",
        example=7
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_oc": 1,
                "numero_oc": "OC-2024-00001",
                "fecha": "2024-01-15T10:30:00",
                "fecha_entrega_esperada": "2024-02-01",
                "estado": "Pendiente",
                "proveedor_nombre": "Ferretería Mayorista SA",
                "sucursal_nombre": "Sucursal Centro",
                "subtotal": 35000.00,
                "iva": 7350.00,
                "descuento": 0.00,
                "total": 42350.00,
                "usuario_nombre": "María Elena Rodríguez",
                "proveedor_info": {
                    "cuit": "30-12345678-9",
                    "contacto": "Juan Pérez",
                    "telefono": "11-1234-5678",
                    "email": "juan@proveedor.com"
                },
                "detalles": [
                    {
                        "id_detalle_oc": 1,
                        "id_producto": 1,
                        "producto_nombre": "Martillo Profesional",
                        "producto_codigo": "MART-001",
                        "unidad_medida": "Unidad",
                        "cantidad": 10,
                        "costo_unitario": 3500.00,
                        "descuento_unitario": 0.00,
                        "subtotal": 35000.00
                    }
                ],
                "dias_transcurridos": 5,
                "tiempo_entrega_estimado": 7,
                "observaciones": "Pedido mensual de herramientas"
            }
        }

# Schema para respuesta de lista de órdenes
class OrdenCompraList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    ordenes: List[OrdenCompraSimple]

    class Config:
        orm_mode = True

# Schema para estadísticas de órdenes de compra
class EstadisticasOC(BaseModel):
    total_ordenes: int
    total_monto: condecimal(decimal_places=2)
    promedio_monto: condecimal(decimal_places=2)
    ordenes_pendientes: int
    ordenes_ultimo_mes: int
    tiempo_promedio_entrega: float
    proveedor_mas_frecuente: str
    productos_mas_pedidos: List[dict]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "total_ordenes": 150,
                "total_monto": 1500000.00,
                "promedio_monto": 10000.00,
                "ordenes_pendientes": 15,
                "ordenes_ultimo_mes": 30,
                "tiempo_promedio_entrega": 5.5,
                "proveedor_mas_frecuente": "Ferretería Mayorista SA",
                "productos_mas_pedidos": [
                    {
                        "producto": "Martillo Profesional",
                        "cantidad_total": 500,
                        "monto_total": 1750000.00
                    }
                ]
            }
        }
