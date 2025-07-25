from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional
from datetime import datetime

class DetalleDevolucionBase(BaseModel):
    id_devolucion: int = Field(
        ...,
        description="ID de la devolución",
        example=1
    )
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
    motivo_especifico: Optional[str] = Field(
        None,
        description="Motivo específico de la devolución del producto",
        example="Producto presenta falla en el mecanismo de ajuste"
    )

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleDevolucionCreate(DetalleDevolucionBase):
    pass

class DetalleDevolucionUpdate(BaseModel):
    cantidad: Optional[int] = Field(None, gt=0)
    motivo_especifico: Optional[str] = None

    @validator('cantidad')
    def validar_cantidad(cls, v):
        if v is not None and v <= 0:
            raise ValueError('La cantidad debe ser mayor a 0')
        return v

class DetalleDevolucionSimple(DetalleDevolucionBase):
    id_detalle_devolucion: int = Field(
        ...,
        description="ID único del detalle de devolución"
    )
    producto_nombre: str = Field(
        ...,
        description="Nombre del producto",
        example="Martillo Profesional"
    )

    class Config:
        orm_mode = True

class DetalleDevolucionCompleto(DetalleDevolucionSimple):
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
    precio_unitario: condecimal(decimal_places=2) = Field(
        ...,
        description="Precio unitario del producto",
        example=4500.00
    )
    subtotal: condecimal(decimal_places=2) = Field(
        ...,
        description="Subtotal del detalle",
        example=4500.00
    )

    # Información adicional
    tiene_garantia: bool = Field(
        ...,
        description="Indica si el producto tiene garantía vigente",
        example=True
    )
    tiempo_garantia_restante: Optional[int] = Field(
        None,
        description="Días restantes de garantía",
        example=360
    )
    dias_desde_compra: int = Field(
        ...,
        description="Días transcurridos desde la compra",
        example=5
    )
    estado_producto: str = Field(
        ...,
        description="Estado en que se recibe el producto",
        example="Sin uso"
    )
    requiere_revision_tecnica: bool = Field(
        ...,
        description="Indica si requiere revisión técnica",
        example=True
    )
    resultado_revision: Optional[str] = Field(
        None,
        description="Resultado de la revisión técnica",
        example="Se confirma defecto de fábrica"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_detalle_devolucion": 1,
                "id_devolucion": 1,
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_categoria": "Herramientas",
                "cantidad": 1,
                "precio_unitario": 4500.00,
                "subtotal": 4500.00,
                "motivo_especifico": "Producto presenta falla en el mecanismo de ajuste",
                "tiene_garantia": True,
                "tiempo_garantia_restante": 360,
                "dias_desde_compra": 5,
                "estado_producto": "Sin uso",
                "requiere_revision_tecnica": True,
                "resultado_revision": "Se confirma defecto de fábrica"
            }
        }

class DetalleDevolucionList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    detalles: list[DetalleDevolucionSimple]

    class Config:
        orm_mode = True

# Schema para resumen de devoluciones por producto
class ResumenDevolucionesProducto(BaseModel):
    id_producto: int
    producto_nombre: str
    total_devoluciones: int
    cantidad_total_devuelta: int
    monto_total_devuelto: condecimal(decimal_places=2)
    motivos_principales: list[dict] = Field(
        ...,
        description="Principales motivos de devolución",
        example=[
            {
                "motivo": "Defecto de fábrica",
                "cantidad": 3,
                "porcentaje": 60.0
            }
        ]
    )
    porcentaje_garantia: float = Field(
        ...,
        description="Porcentaje de devoluciones por garantía",
        example=80.0
    )
    tiempo_promedio_uso: float = Field(
        ...,
        description="Promedio de días entre compra y devolución",
        example=5.5
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_producto": 1,
                "producto_nombre": "Martillo Profesional",
                "total_devoluciones": 5,
                "cantidad_total_devuelta": 5,
                "monto_total_devuelto": 22500.00,
                "motivos_principales": [
                    {
                        "motivo": "Defecto de fábrica",
                        "cantidad": 3,
                        "porcentaje": 60.0
                    }
                ],
                "porcentaje_garantia": 80.0,
                "tiempo_promedio_uso": 5.5
            }
        }

# Schema para análisis técnico de devoluciones
class AnalisisTecnicoDevolucion(BaseModel):
    id_detalle_devolucion: int
    producto_info: dict = Field(
        ...,
        example={
            "id": 1,
            "nombre": "Martillo Profesional",
            "codigo": "MART-001",
            "categoria": "Herramientas",
            "fabricante": "Tools Pro"
        }
    )
    detalles_revision: dict = Field(
        ...,
        example={
            "fecha_revision": "2024-01-21T10:00:00",
            "tecnico": "Juan Técnico",
            "estado_producto": "Sin uso",
            "falla_confirmada": True,
            "tipo_falla": "Defecto de fabricación",
            "detalles": "Se confirma falla en el mecanismo de ajuste",
            "reparable": False,
            "fotos": ["foto1.jpg", "foto2.jpg"],
            "recomendacion": "Reemplazo total del producto"
        }
    )
    resolucion: dict = Field(
        ...,
        example={
            "tipo": "Reemplazo",
            "aprobado": True,
            "fecha_resolucion": "2024-01-21T11:00:00",
            "autorizado_por": "María Supervisora",
            "observaciones": "Se autoriza reemplazo por unidad nueva"
        }
    )

    class Config:
        orm_mode = True
