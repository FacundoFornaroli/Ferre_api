from pydantic import BaseModel, Field, validator, constr
from typing import Optional, List
from datetime import datetime

class DetalleTransferenciaBase(BaseModel):
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

# Schema para Crear Detalle
class DetalleTransferenciaCreate(DetalleTransferenciaBase):
    pass

class TransferenciaSucursalBase(BaseModel):
    id_sucursal_origen: int = Field(
        ...,
        description="ID de la sucursal origen",
        example=1
    )
    id_sucursal_destino: int = Field(
        ...,
        description="ID de la sucursal destino",
        example=2
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones de la transferencia",
        example="Transferencia urgente para reposición de stock"
    )

    @validator('id_sucursal_destino')
    def validar_sucursales_diferentes(cls, v, values):
        if 'id_sucursal_origen' in values and v == values['id_sucursal_origen']:
            raise ValueError('La sucursal de origen y destino no pueden ser la misma')
        return v

class TransferenciaSucursalCreate(TransferenciaSucursalBase):
    detalles: List[DetalleTransferenciaCreate]

class TransferenciaSucursalUpdate(BaseModel):
    estado: Optional[str] = Field(
        None,
        description="Estado de la transferencia"
    )
    id_usuario_autorizador: Optional[int] = None
    observaciones: Optional[str] = None

    @validator('estado')
    def validar_estado(cls, v):
        if v:
            estados_validos = ['Pendiente', 'Aprobada', 'En Tránsito', 'Completada', 'Cancelada']
            if v not in estados_validos:
                raise ValueError(f'Estado debe ser uno de: {", ".join(estados_validos)}')
        return v

class DetalleTransferenciaResponse(DetalleTransferenciaBase):
    id_detalle_transferencia: int
    cantidad_recibida: Optional[int] = Field(None, example=10)
    producto_nombre: str = Field(..., example="Martillo Profesional")
    producto_codigo: Optional[str] = Field(None, example="MART-001")
    stock_origen: int = Field(..., example=50)
    stock_destino: int = Field(..., example=5)

    @validator('cantidad_recibida')
    def validar_cantidad_recibida(cls, v, values):
        if v is not None and 'cantidad' in values and v > values['cantidad']:
            raise ValueError('La cantidad recibida no puede ser mayor a la cantidad enviada')
        return v

    class Config:
        from_attributes = True

class TransferenciaSucursalSimple(TransferenciaSucursalBase):
    id_transferencia: int = Field(..., description="ID único de la transferencia")
    numero_transferencia: Optional[str] = Field(None, example="TR-2024-00001")
    fecha_solicitud: datetime
    estado: str = Field(..., example="Pendiente")
    total_items: int = Field(..., example=2)
    sucursal_origen_nombre: str = Field(..., example="Sucursal Centro")
    sucursal_destino_nombre: str = Field(..., example="Sucursal Norte")

    class Config:
        from_attributes = True

class TransferenciaSucursalCompleta(TransferenciaSucursalSimple):
    fecha_transferencia: Optional[datetime] = None
    usuario_solicitante_nombre: str = Field(..., example="Juan Pérez")
    usuario_autorizador_nombre: Optional[str] = Field(None, example="María Supervisora")
    detalles: List[DetalleTransferenciaResponse]
    tiempo_transito_estimado: Optional[int] = Field(
        None,
        description="Tiempo estimado de tránsito en horas",
        example=24
    )
    prioridad: str = Field(
        "Normal",
        description="Prioridad de la transferencia",
        example="Alta"
    )
    motivo_prioridad: Optional[str] = Field(
        None,
        description="Motivo de la prioridad asignada",
        example="Stock crítico en sucursal destino"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_transferencia": 1,
                "numero_transferencia": "TR-2024-00001",
                "fecha_solicitud": "2024-01-15T10:30:00",
                "fecha_transferencia": "2024-01-15T14:30:00",
                "estado": "En Tránsito",
                "id_sucursal_origen": 1,
                "id_sucursal_destino": 2,
                "sucursal_origen_nombre": "Sucursal Centro",
                "sucursal_destino_nombre": "Sucursal Norte",
                "usuario_solicitante_nombre": "Juan Pérez",
                "usuario_autorizador_nombre": "María Supervisora",
                "total_items": 2,
                "tiempo_transito_estimado": 24,
                "prioridad": "Alta",
                "motivo_prioridad": "Stock crítico en sucursal destino",
                "detalles": [
                    {
                        "id_detalle_transferencia": 1,
                        "id_producto": 1,
                        "producto_nombre": "Martillo Profesional",
                        "producto_codigo": "MART-001",
                        "cantidad": 10,
                        "cantidad_recibida": None,
                        "stock_origen": 50,
                        "stock_destino": 5
                    }
                ],
                "observaciones": "Transferencia urgente para reposición de stock"
            }
        }

class TransferenciaSucursalList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    transferencias: List[TransferenciaSucursalSimple]

    class Config:
        from_attributes = True

# Schema para estadísticas de transferencias
class EstadisticasTransferencias(BaseModel):
    periodo: str = Field(..., example="2024-01")
    total_transferencias: int
    transferencias_por_estado: dict = Field(
        ...,
        example={
            "Pendiente": 5,
            "Aprobada": 3,
            "En Tránsito": 2,
            "Completada": 15,
            "Cancelada": 1
        }
    )
    tiempo_promedio_proceso: dict = Field(
        ...,
        example={
            "aprobacion": 2.5,  # horas
            "preparacion": 1.5,  # horas
            "transito": 24.0,   # horas
            "recepcion": 1.0    # horas
        }
    )
    productos_mas_transferidos: List[dict] = Field(
        ...,
        example=[
            {
                "producto": "Martillo Profesional",
                "cantidad_total": 50,
                "transferencias": 5
            }
        ]
    )
    sucursales_mas_activas: dict = Field(
        ...,
        example={
            "origen": [
                {
                    "sucursal": "Sucursal Centro",
                    "transferencias": 15,
                    "productos": 150
                }
            ],
            "destino": [
                {
                    "sucursal": "Sucursal Norte",
                    "transferencias": 10,
                    "productos": 100
                }
            ]
        }
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "periodo": "2024-01",
                "total_transferencias": 26,
                "transferencias_por_estado": {
                    "Pendiente": 5,
                    "Aprobada": 3,
                    "En Tránsito": 2,
                    "Completada": 15,
                    "Cancelada": 1
                },
                "tiempo_promedio_proceso": {
                    "aprobacion": 2.5,
                    "preparacion": 1.5,
                    "transito": 24.0,
                    "recepcion": 1.0
                },
                "productos_mas_transferidos": [
                    {
                        "producto": "Martillo Profesional",
                        "cantidad_total": 50,
                        "transferencias": 5
                    }
                ],
                "sucursales_mas_activas": {
                    "origen": [
                        {
                            "sucursal": "Sucursal Centro",
                            "transferencias": 15,
                            "productos": 150
                        }
                    ],
                    "destino": [
                        {
                            "sucursal": "Sucursal Norte",
                            "transferencias": 10,
                            "productos": 100
                        }
                    ]
                }
            }
        }
