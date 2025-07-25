from pydantic import BaseModel, Field, validator, condecimal, constr
from typing import Optional, List
from datetime import date

class DescuentoBase(BaseModel):
    nombre: constr(max_length=100) = Field(
        ...,
        description="Nombre del descuento",
        example="Descuento Black Friday"
    )
    descripcion: Optional[str] = Field(
        None,
        description="Descripción detallada del descuento",
        example="Descuento especial por Black Friday en herramientas seleccionadas"
    )
    porcentaje: condecimal(ge=0, le=100, decimal_places=2) = Field(
        ...,
        description="Porcentaje de descuento",
        example=15.00
    )
    monto_fijo: Optional[condecimal(ge=0, decimal_places=2)] = Field(
        None,
        description="Monto fijo de descuento",
        example=1000.00
    )
    tipo_descuento: constr(max_length=20) = Field(
        ...,
        description="Tipo de descuento",
        example="Porcentaje"
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
    cantidad_minima: Optional[int] = Field(
        None,
        description="Cantidad mínima de productos para aplicar el descuento",
        example=2,
        ge=1
    )
    cantidad_maxima: Optional[int] = Field(
        None,
        description="Cantidad máxima de productos con descuento",
        example=5,
        ge=1
    )

    @validator('tipo_descuento')
    def validar_tipo_descuento(cls, v):
        tipos_validos = ['Porcentaje', 'Monto Fijo']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de descuento debe ser uno de: {", ".join(tipos_validos)}')
        return v

    @validator('fecha_fin')
    def validar_fecha_fin(cls, v, values):
        if 'fecha_inicio' in values and v < values['fecha_inicio']:
            raise ValueError('La fecha de fin no puede ser anterior a la fecha de inicio')
        return v

    @validator('cantidad_maxima')
    def validar_cantidad_maxima(cls, v, values):
        if v is not None and 'cantidad_minima' in values and values['cantidad_minima'] is not None:
            if v < values['cantidad_minima']:
                raise ValueError('La cantidad máxima debe ser mayor o igual a la cantidad mínima')
        return v

    @validator('monto_fijo')
    def validar_monto_tipo(cls, v, values):
        if 'tipo_descuento' in values:
            if values['tipo_descuento'] == 'Monto Fijo' and v is None:
                raise ValueError('Debe especificar un monto fijo para descuentos de tipo Monto Fijo')
            elif values['tipo_descuento'] == 'Porcentaje' and v is not None:
                raise ValueError('No debe especificar monto fijo para descuentos de tipo Porcentaje')
        return v

class ProductoDescuentoBase(BaseModel):
    id_producto: int = Field(
        ...,
        description="ID del producto",
        example=1
    )

class DescuentoCreate(DescuentoBase):
    productos: List[ProductoDescuentoBase]

class DescuentoUpdate(BaseModel):
    nombre: Optional[constr(max_length=100)] = None
    descripcion: Optional[str] = None
    porcentaje: Optional[condecimal(ge=0, le=100, decimal_places=2)] = None
    monto_fijo: Optional[condecimal(ge=0, decimal_places=2)] = None
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    cantidad_minima: Optional[int] = Field(None, ge=1)
    cantidad_maxima: Optional[int] = Field(None, ge=1)
    activo: Optional[bool] = None

    @validator('fecha_fin')
    def validar_fecha_fin(cls, v, values):
        if v is not None and 'fecha_inicio' in values and values['fecha_inicio'] is not None:
            if v < values['fecha_inicio']:
                raise ValueError('La fecha de fin no puede ser anterior a la fecha de inicio')
        return v

class DescuentoSimple(DescuentoBase):
    id_descuento: int = Field(..., description="ID único del descuento")
    activo: bool
    cantidad_productos: int = Field(
        0,
        description="Cantidad de productos incluidos en el descuento",
        example=10
    )

    class Config:
        orm_mode = True

class ProductoDescuentoResponse(BaseModel):
    id_producto: int
    nombre: str = Field(..., example="Martillo Profesional")
    codigo: Optional[str] = Field(None, example="MART-001")
    precio_original: condecimal(decimal_places=2) = Field(..., example=4500.00)
    precio_con_descuento: condecimal(decimal_places=2) = Field(..., example=3825.00)
    ahorro: condecimal(decimal_places=2) = Field(..., example=675.00)

    class Config:
        orm_mode = True

class DescuentoCompleto(DescuentoSimple):
    productos: List[ProductoDescuentoResponse]
    total_aplicaciones: int = Field(
        0,
        description="Cantidad de veces que se ha aplicado el descuento",
        example=45
    )
    ahorro_total_generado: condecimal(decimal_places=2) = Field(
        0,
        description="Monto total ahorrado por los clientes con este descuento",
        example=30375.00
    )
    dias_restantes: int = Field(
        ...,
        description="Días restantes de vigencia",
        example=15
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_descuento": 1,
                "nombre": "Descuento Black Friday",
                "descripcion": "Descuento especial por Black Friday en herramientas seleccionadas",
                "porcentaje": 15.00,
                "monto_fijo": None,
                "tipo_descuento": "Porcentaje",
                "fecha_inicio": "2024-01-15",
                "fecha_fin": "2024-01-31",
                "cantidad_minima": 2,
                "cantidad_maxima": 5,
                "activo": True,
                "cantidad_productos": 10,
                "total_aplicaciones": 45,
                "ahorro_total_generado": 30375.00,
                "dias_restantes": 15,
                "productos": [
                    {
                        "id_producto": 1,
                        "nombre": "Martillo Profesional",
                        "codigo": "MART-001",
                        "precio_original": 4500.00,
                        "precio_con_descuento": 3825.00,
                        "ahorro": 675.00
                    }
                ]
            }
        }

class DescuentoList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    descuentos: List[DescuentoSimple]

    class Config:
        orm_mode = True

# Schema para estadísticas de descuentos
class EstadisticasDescuentos(BaseModel):
    descuentos_activos: int
    total_productos_con_descuento: int
    ahorro_total_mes: condecimal(decimal_places=2)
    promedio_descuento: condecimal(decimal_places=2)
    descuentos_mas_usados: List[dict]
    productos_mas_descontados: List[dict]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "descuentos_activos": 15,
                "total_productos_con_descuento": 150,
                "ahorro_total_mes": 125000.00,
                "promedio_descuento": 15.50,
                "descuentos_mas_usados": [
                    {
                        "nombre": "Descuento Black Friday",
                        "aplicaciones": 45,
                        "ahorro_generado": 30375.00
                    }
                ],
                "productos_mas_descontados": [
                    {
                        "producto": "Martillo Profesional",
                        "veces_descontado": 25,
                        "ahorro_total": 16875.00
                    }
                ]
            }
        }
