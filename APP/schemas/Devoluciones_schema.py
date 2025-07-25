from pydantic import BaseModel, Field, validator, constr
from typing import Optional, List
from datetime import datetime

class DetalleDevolucionBase(BaseModel):
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    cantidad: int = Field(
        ...,
        description="Cantidad a devolver",
        example=1,
        gt=0  # greater than 0
    )
    motivo_especifico: Optional[constr(max_length=200)] = Field(
        None,
        description="Motivo específico de la devolución del producto",
        example="Producto presenta falla en el mecanismo de ajuste"
    )

class DevolucionBase(BaseModel):
    id_factura_venta: int = Field(
        ...,
        description="ID de la factura de venta",
        example=1
    )
    motivo: constr(max_length=200) = Field(
        ...,
        description="Motivo general de la devolución",
        example="Producto defectuoso"
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones adicionales",
        example="Cliente reporta falla inmediata al primer uso"
    )

class DevolucionCreate(DevolucionBase):
    detalles: List[DetalleDevolucionBase]

class DevolucionUpdate(BaseModel):
    estado: Optional[str] = Field(
        None,
        description="Estado de la devolución"
    )
    observaciones: Optional[str] = None

    @validator('estado')
    def validar_estado(cls, v):
        if v:
            estados_validos = ['Pendiente', 'Aprobada', 'Rechazada', 'Completada']
            if v not in estados_validos:
                raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v

class DetalleDevolucionResponse(DetalleDevolucionBase):
    id_detalle_devolucion: int
    producto_nombre: str = Field(..., example="Martillo Profesional")
    producto_codigo: Optional[str] = Field(None, example="MART-001")
    precio_unitario: float = Field(..., example=4500.00)
    subtotal: float = Field(..., example=4500.00)
    tiene_garantia: bool = Field(..., example=True)
    dias_desde_compra: int = Field(..., example=5)

    class Config:
        orm_mode = True

class DevolucionSimple(DevolucionBase):
    id_devolucion: int = Field(..., description="ID único de la devolución")
    fecha_devolucion: datetime
    estado: str = Field(..., example="Pendiente")
    cliente_nombre: str = Field(..., example="Juan Pérez")
    numero_factura: str = Field(..., example="A-0001-00000001")
    total_items: int = Field(..., example=1)

    class Config:
        orm_mode = True

class DevolucionCompleta(DevolucionSimple):
    detalles: List[DetalleDevolucionResponse]
    factura_fecha: datetime
    sucursal_nombre: str = Field(..., example="Sucursal Centro")
    usuario_nombre: str = Field(..., example="María Rodríguez")
    total_devolucion: float = Field(..., example=4500.00)
    afecta_stock: bool = Field(
        ...,
        description="Indica si la devolución afecta al stock",
        example=True
    )
    requiere_inspeccion_tecnica: bool = Field(
        ...,
        description="Indica si requiere revisión técnica",
        example=True
    )
    dias_desde_compra: int = Field(
        ...,
        description="Días transcurridos desde la compra",
        example=5
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_devolucion": 1,
                "fecha_devolucion": "2024-01-20T10:30:00",
                "id_factura_venta": 1,
                "numero_factura": "A-0001-00000001",
                "factura_fecha": "2024-01-15T15:30:00",
                "cliente_nombre": "Juan Pérez",
                "sucursal_nombre": "Sucursal Centro",
                "usuario_nombre": "María Rodríguez",
                "estado": "Pendiente",
                "motivo": "Producto defectuoso",
                "total_items": 1,
                "total_devolucion": 4500.00,
                "afecta_stock": True,
                "requiere_inspeccion_tecnica": True,
                "dias_desde_compra": 5,
                "detalles": [
                    {
                        "id_detalle_devolucion": 1,
                        "id_producto": 1,
                        "producto_nombre": "Martillo Profesional",
                        "producto_codigo": "MART-001",
                        "cantidad": 1,
                        "precio_unitario": 4500.00,
                        "subtotal": 4500.00,
                        "motivo_especifico": "Producto presenta falla en el mecanismo de ajuste",
                        "tiene_garantia": True,
                        "dias_desde_compra": 5
                    }
                ],
                "observaciones": "Cliente reporta falla inmediata al primer uso"
            }
        }

class DevolucionList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    devoluciones: List[DevolucionSimple]

    class Config:
        orm_mode = True

# Schema para estadísticas de devoluciones
class EstadisticasDevoluciones(BaseModel):
    periodo: str = Field(..., example="2024-01")
    total_devoluciones: int
    monto_total_devuelto: float
    porcentaje_ventas: float
    devoluciones_por_estado: dict = Field(
        ...,
        example={
            "Pendiente": 5,
            "Aprobada": 10,
            "Rechazada": 2,
            "Completada": 8
        }
    )
    motivos_principales: List[dict] = Field(
        ...,
        example=[
            {
                "motivo": "Producto defectuoso",
                "cantidad": 15,
                "porcentaje": 60.0
            }
        ]
    )
    productos_mas_devueltos: List[dict] = Field(
        ...,
        example=[
            {
                "producto": "Martillo Profesional",
                "cantidad": 3,
                "monto": 13500.00,
                "motivo_principal": "Defecto de fábrica"
            }
        ]
    )
    tiempo_promedio_procesamiento: float = Field(
        ...,
        description="Tiempo promedio en días para procesar una devolución",
        example=2.5
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "periodo": "2024-01",
                "total_devoluciones": 25,
                "monto_total_devuelto": 112500.00,
                "porcentaje_ventas": 5.5,
                "devoluciones_por_estado": {
                    "Pendiente": 5,
                    "Aprobada": 10,
                    "Rechazada": 2,
                    "Completada": 8
                },
                "motivos_principales": [
                    {
                        "motivo": "Producto defectuoso",
                        "cantidad": 15,
                        "porcentaje": 60.0
                    }
                ],
                "productos_mas_devueltos": [
                    {
                        "producto": "Martillo Profesional",
                        "cantidad": 3,
                        "monto": 13500.00,
                        "motivo_principal": "Defecto de fábrica"
                    }
                ],
                "tiempo_promedio_procesamiento": 2.5
            }
        }
