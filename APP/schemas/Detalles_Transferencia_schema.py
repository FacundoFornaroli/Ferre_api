from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional, List
from datetime import datetime

class DetalleTransferenciaBase(BaseModel):
    id_transferencia: int = Field(
        ...,
        description="ID de la transferencia",
        example=1
    )
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    cantidad: int = Field(
        ...,
        description="Cantidad a transferir",
        example=10,
        gt=0  # greater than 0
    )

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleTransferenciaCreate(DetalleTransferenciaBase):
    pass

class DetalleTransferenciaUpdate(BaseModel):
    cantidad_recibida: Optional[int] = Field(
        None,
        description="Cantidad recibida en destino",
        example=10,
        ge=0  # greater or equal than 0
    )

    @validator('cantidad_recibida')
    def validar_cantidad_recibida(cls, v):
        if v is not None and v < 0:
            raise ValueError('La cantidad recibida no puede ser negativa')
        return v

class DetalleTransferenciaSimple(DetalleTransferenciaBase):
    id_detalle_transferencia: int = Field(
        ...,
        description="ID único del detalle de transferencia"
    )
    cantidad_recibida: Optional[int] = None
    producto_nombre: str = Field(
        ...,
        description="Nombre del producto",
        example="Martillo Profesional"
    )

    class Config:
        from_attributes = True

class DetalleTransferenciaCompleto(DetalleTransferenciaSimple):
    # Información del Producto
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
    
    # Información de Stock
    stock_origen_inicial: int = Field(
        ...,
        description="Stock en sucursal origen al momento de la transferencia",
        example=50
    )
    stock_origen_actual: int = Field(
        ...,
        description="Stock actual en sucursal origen",
        example=40
    )
    stock_destino_inicial: int = Field(
        ...,
        description="Stock en sucursal destino al momento de la transferencia",
        example=5
    )
    stock_destino_actual: int = Field(
        ...,
        description="Stock actual en sucursal destino",
        example=15
    )

    # Información de Seguimiento
    estado_item: str = Field(
        ...,
        description="Estado específico del ítem",
        example="En Tránsito"
    )
    fecha_preparacion: Optional[datetime] = Field(
        None,
        description="Fecha de preparación del ítem",
        example="2024-01-15T11:30:00"
    )
    fecha_recepcion: Optional[datetime] = Field(
        None,
        description="Fecha de recepción del ítem",
        example="2024-01-15T15:30:00"
    )
    diferencia_cantidad: Optional[int] = Field(
        None,
        description="Diferencia entre cantidad enviada y recibida",
        example=0
    )
    motivo_diferencia: Optional[str] = Field(
        None,
        description="Motivo de la diferencia si existe",
        example="Sin diferencias"
    )
    observaciones_item: Optional[str] = Field(
        None,
        description="Observaciones específicas del ítem",
        example="Producto embalado correctamente"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_detalle_transferencia": 1,
                "id_transferencia": 1,
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_categoria": "Herramientas",
                "unidad_medida": "Unidad",
                "cantidad": 10,
                "cantidad_recibida": 10,
                "stock_origen_inicial": 50,
                "stock_origen_actual": 40,
                "stock_destino_inicial": 5,
                "stock_destino_actual": 15,
                "estado_item": "Completado",
                "fecha_preparacion": "2024-01-15T11:30:00",
                "fecha_recepcion": "2024-01-15T15:30:00",
                "diferencia_cantidad": 0,
                "motivo_diferencia": "Sin diferencias",
                "observaciones_item": "Producto embalado correctamente"
            }
        }

class DetalleTransferenciaList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    detalles: List[DetalleTransferenciaSimple]

    class Config:
        from_attributes = True

# Schema para seguimiento detallado del ítem
class SeguimientoDetalleTransferencia(BaseModel):
    id_detalle_transferencia: int
    numero_transferencia: str
    producto_info: dict = Field(
        ...,
        example={
            "nombre": "Martillo Profesional",
            "codigo": "MART-001",
            "categoria": "Herramientas"
        }
    )
    cantidades: dict = Field(
        ...,
        example={
            "solicitada": 10,
            "preparada": 10,
            "en_transito": 10,
            "recibida": 10
        }
    )
    estados: List[dict] = Field(
        ...,
        example=[
            {
                "estado": "Solicitado",
                "fecha": "2024-01-15T10:30:00",
                "usuario": "Juan Pérez",
                "observaciones": "Solicitud inicial"
            },
            {
                "estado": "Preparado",
                "fecha": "2024-01-15T11:30:00",
                "usuario": "Pedro Almacén",
                "observaciones": "Producto embalado"
            },
            {
                "estado": "En Tránsito",
                "fecha": "2024-01-15T12:30:00",
                "usuario": "Carlos Transporte",
                "observaciones": "En camino"
            },
            {
                "estado": "Recibido",
                "fecha": "2024-01-15T15:30:00",
                "usuario": "Ana Recepción",
                "observaciones": "Recibido conforme"
            }
        ]
    )

    class Config:
        from_attributes = True

# Schema para análisis de transferencias por producto
class AnalisisTransferenciasProducto(BaseModel):
    id_producto: int
    producto_info: dict
    transferencias_totales: int
    cantidad_total_transferida: int
    tiempo_promedio_transito: float
    sucursales_origen_frecuentes: List[dict]
    sucursales_destino_frecuentes: List[dict]
    historial_mensual: List[dict]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_producto": 1,
                "producto_info": {
                    "nombre": "Martillo Profesional",
                    "codigo": "MART-001",
                    "categoria": "Herramientas"
                },
                "transferencias_totales": 15,
                "cantidad_total_transferida": 150,
                "tiempo_promedio_transito": 24.5,
                "sucursales_origen_frecuentes": [
                    {
                        "sucursal": "Sucursal Centro",
                        "cantidad": 100,
                        "transferencias": 10
                    }
                ],
                "sucursales_destino_frecuentes": [
                    {
                        "sucursal": "Sucursal Norte",
                        "cantidad": 80,
                        "transferencias": 8
                    }
                ],
                "historial_mensual": [
                    {
                        "mes": "2024-01",
                        "cantidad": 50,
                        "transferencias": 5
                    }
                ]
            }
        }
