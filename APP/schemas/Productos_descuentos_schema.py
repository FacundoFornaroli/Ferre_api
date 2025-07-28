from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional, List
from datetime import datetime, date

class ProductoDescuentoBase(BaseModel):
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )
    id_descuento: int = Field(
        ...,
        description="ID del descuento",
        example=1
    )

class ProductoDescuentoCreate(ProductoDescuentoBase):
    pass

class ProductoDescuentoUpdate(BaseModel):
    pass  # No se permiten actualizaciones directas en esta tabla de relación

class ProductoDescuentoSimple(ProductoDescuentoBase):
    id_producto_descuento: int = Field(
        ...,
        description="ID único de la relación producto-descuento"
    )

    class Config:
        from_attributes = True

class ProductoDescuentoCompleto(ProductoDescuentoSimple):
    # Información del Producto
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
    producto_precio: condecimal(decimal_places=2) = Field(
        ...,
        description="Precio original del producto",
        example=4500.00
    )
    
    # Información del Descuento
    descuento_nombre: str = Field(
        ...,
        description="Nombre del descuento",
        example="Descuento Black Friday"
    )
    descuento_tipo: str = Field(
        ...,
        description="Tipo de descuento",
        example="Porcentaje"
    )
    descuento_valor: condecimal(decimal_places=2) = Field(
        ...,
        description="Valor del descuento (porcentaje o monto fijo)",
        example=15.00
    )
    fecha_inicio: date = Field(
        ...,
        description="Fecha de inicio del descuento",
        example="2024-01-15"
    )
    fecha_fin: date = Field(
        ...,
        description="Fecha de fin del descuento",
        example="2024-01-31"
    )
    
    # Campos calculados
    precio_con_descuento: condecimal(decimal_places=2) = Field(
        ...,
        description="Precio final con descuento aplicado",
        example=3825.00
    )
    ahorro: condecimal(decimal_places=2) = Field(
        ...,
        description="Monto de ahorro",
        example=675.00
    )
    dias_restantes: int = Field(
        ...,
        description="Días restantes de vigencia del descuento",
        example=15
    )
    veces_aplicado: int = Field(
        0,
        description="Cantidad de veces que se ha aplicado este descuento al producto",
        example=12
    )
    ahorro_total_generado: condecimal(decimal_places=2) = Field(
        0,
        description="Monto total ahorrado por los clientes en este producto con este descuento",
        example=8100.00
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_producto_descuento": 1,
                "id_producto": 1,
                "id_descuento": 1,
                "producto_nombre": "Martillo Profesional",
                "producto_codigo": "MART-001",
                "producto_precio": 4500.00,
                "descuento_nombre": "Descuento Black Friday",
                "descuento_tipo": "Porcentaje",
                "descuento_valor": 15.00,
                "fecha_inicio": "2024-01-15",
                "fecha_fin": "2024-01-31",
                "precio_con_descuento": 3825.00,
                "ahorro": 675.00,
                "dias_restantes": 15,
                "veces_aplicado": 12,
                "ahorro_total_generado": 8100.00
            }
        }

class ProductoDescuentoList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    productos_descuentos: List[ProductoDescuentoSimple]

    class Config:
        from_attributes = True

# Schema para resumen de descuentos por producto
class ResumenDescuentosProducto(BaseModel):
    id_producto: int
    nombre_producto: str
    codigo_producto: Optional[str]
    precio_original: condecimal(decimal_places=2)
    descuentos_activos: List[dict] = Field(
        ...,
        description="Lista de descuentos activos para el producto",
        example=[
            {
                "id_descuento": 1,
                "nombre": "Descuento Black Friday",
                "tipo": "Porcentaje",
                "valor": 15.00,
                "precio_final": 3825.00,
                "fecha_fin": "2024-01-31"
            }
        ]
    )
    mejor_precio_actual: condecimal(decimal_places=2) = Field(
        ...,
        description="Mejor precio disponible con descuentos",
        example=3825.00
    )
    historial_descuentos: List[dict] = Field(
        ...,
        description="Historial de descuentos aplicados",
        example=[
            {
                "periodo": "2024-01",
                "descuentos_aplicados": 3,
                "ahorro_total": 2025.00,
                "ventas_con_descuento": 12
            }
        ]
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_producto": 1,
                "nombre_producto": "Martillo Profesional",
                "codigo_producto": "MART-001",
                "precio_original": 4500.00,
                "descuentos_activos": [
                    {
                        "id_descuento": 1,
                        "nombre": "Descuento Black Friday",
                        "tipo": "Porcentaje",
                        "valor": 15.00,
                        "precio_final": 3825.00,
                        "fecha_fin": "2024-01-31"
                    }
                ],
                "mejor_precio_actual": 3825.00,
                "historial_descuentos": [
                    {
                        "periodo": "2024-01",
                        "descuentos_aplicados": 3,
                        "ahorro_total": 2025.00,
                        "ventas_con_descuento": 12
                    }
                ]
            }
        }

# Schema para análisis de efectividad de descuentos
class AnalisisEfectividadDescuentos(BaseModel):
    periodo: str = Field(..., example="2024-01")
    productos_con_descuento: int
    ventas_con_descuento: int
    ventas_sin_descuento: int
    incremento_ventas: float  # porcentaje
    ahorro_total: condecimal(decimal_places=2)
    margen_promedio: float  # porcentaje
    productos_destacados: List[dict]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "periodo": "2024-01",
                "productos_con_descuento": 50,
                "ventas_con_descuento": 150,
                "ventas_sin_descuento": 100,
                "incremento_ventas": 50.0,
                "ahorro_total": 45000.00,
                "margen_promedio": 25.5,
                "productos_destacados": [
                    {
                        "producto": "Martillo Profesional",
                        "incremento_ventas": 75.0,
                        "ahorro_generado": 8100.00,
                        "efectividad": "Alta"
                    }
                ]
            }
        }
