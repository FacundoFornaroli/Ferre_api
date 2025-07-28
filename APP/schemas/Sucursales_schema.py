from pydantic import BaseModel, Field, constr, validator
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, time

# Schema Base
class SucursalBase(BaseModel):
    nombre: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Nombre de la sucursal",
        example="Sucursal Centro"
    )
    direccion: constr(min_length=5, max_length=200, strip_whitespace=True) = Field(
        ...,
        description="Dirección completa de la sucursal",
        example="Av. Principal 123"
    )
    telefono: Optional[constr(max_length=40, strip_whitespace=True)] = Field(
        None,
        description="Número de teléfono de la sucursal",
        example="351-4567890"
    )
    email: Optional[constr(max_length=120, strip_whitespace=True)] = Field(
        None,
        description="Email de contacto de la sucursal",
        example="sucursal.centro@ferreteria.com"
    )
    localidad: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Localidad donde se encuentra la sucursal",
        example="Córdoba"
    )
    provincia: constr(min_length=2, max_length=50, strip_whitespace=True) = Field(
        ...,
        description="Provincia donde se encuentra la sucursal",
        example="Córdoba"
    )
    codigo_postal: Optional[constr(max_length=10, strip_whitespace=True)] = Field(
        None,
        description="Código postal de la sucursal",
        example="5000"
    )
    horario_apertura: Optional[time] = Field(
        None,
        description="Hora de apertura de la sucursal",
        example="08:00"
    )
    horario_cierre: Optional[time] = Field(
        None,
        description="Hora de cierre de la sucursal",
        example="18:00"
    )

    @validator('horario_cierre')
    def validar_horarios(cls, v, values):
        if v and 'horario_apertura' in values and values['horario_apertura']:
            if v <= values['horario_apertura']:
                raise ValueError('El horario de cierre debe ser posterior al de apertura')
        return v

    @validator('email')
    def validar_email(cls, v):
        if v:
            if '@' not in v or '.' not in v:
                raise ValueError('Email inválido')
        return v.lower() if v else v

# Schema para Crear
class SucursalCreate(SucursalBase):
    pass

# Schema para Actualizar
class SucursalUpdate(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=100)] = None
    direccion: Optional[constr(min_length=5, max_length=200)] = None
    telefono: Optional[constr(max_length=40)] = None
    email: Optional[constr(max_length=120)] = None
    localidad: Optional[constr(min_length=2, max_length=100)] = None
    provincia: Optional[constr(min_length=2, max_length=50)] = None
    codigo_postal: Optional[constr(max_length=10)] = None
    horario_apertura: Optional[time] = None
    horario_cierre: Optional[time] = None
    activo: Optional[bool] = None

# Schema para respuesta básica
class SucursalSimple(SucursalBase):
    id_sucursal: int = Field(
        ...,
        description="ID único de la sucursal",
        example=1
    )
    activo: bool

    class Config:
        from_attributes = True

# Schema para respuesta completa
class SucursalCompleta(SucursalSimple):
    fecha_creacion: datetime
    usuarios_count: int = Field(
        0,
        description="Cantidad de usuarios asignados a la sucursal",
        example=5
    )
    inventario_count: int = Field(
        0,
        description="Cantidad de productos en inventario",
        example=100
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_sucursal": 1,
                "nombre": "Sucursal Centro",
                "direccion": "Av. Principal 123",
                "telefono": "351-4567890",
                "email": "sucursal.centro@ferreteria.com",
                "localidad": "Córdoba",
                "provincia": "Córdoba",
                "codigo_postal": "5000",
                "horario_apertura": "08:00",
                "horario_cierre": "18:00",
                "activo": True,
                "fecha_creacion": "2024-01-20T10:00:00",
                "usuarios_count": 5,
                "inventario_count": 100
            }
        }

# Schema para lista paginada de sucursales
class SucursalList(BaseModel):
    total: int = Field(..., description="Total de registros")
    pagina: int = Field(..., description="Página actual")
    paginas: int = Field(..., description="Total de páginas")
    items: List[SucursalSimple]

    class Config:
        from_attributes = True
