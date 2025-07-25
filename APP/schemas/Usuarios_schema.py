from pydantic import BaseModel, Field, constr, validator, EmailStr
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

# Schema Base
class UsuarioBase(BaseModel):
    nombre: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Nombre del usuario",
        example="Juan"
    )
    apellido: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Apellido del usuario",
        example="Pérez"
    )
    cuil: Optional[constr(max_length=13, strip_whitespace=True)] = Field(
        None,
        description="CUIL del usuario",
        example="20-12345678-9"
    )
    rol: constr(max_length=50) = Field(
        ...,
        description="Rol del usuario en el sistema",
        example="Vendedor"
    )
    email: EmailStr = Field(
        ...,
        description="Email del usuario",
        example="juan.perez@ferreteria.com"
    )
    id_sucursal: Optional[int] = Field(
        None,
        description="ID de la sucursal asignada",
        example=1
    )

    @validator('cuil')
    def validar_cuil(cls, v):
        if v:
            # Eliminar guiones y espacios
            v = v.replace('-', '').replace(' ', '')
            if not v.isdigit() or len(v) != 11:
                raise ValueError('CUIL inválido')
            # Reformatear como XX-XXXXXXXX-X
            return f"{v[:2]}-{v[2:10]}-{v[10]}"
        return v

    @validator('rol')
    def validar_rol(cls, v):
        roles_validos = ['Admin', 'Gerente', 'Vendedor', 'Almacén', 'Contador']
        if v not in roles_validos:
            raise ValueError(f'Rol debe ser uno de: {", ".join(roles_validos)}')
        return v

# Schema para Crear (incluye contraseña)
class UsuarioCreate(UsuarioBase):
    contraseña: constr(min_length=8) = Field(
        ...,
        description="Contraseña del usuario (mínimo 8 caracteres)",
        example="contraseña123"
    )

# Schema para Actualizar
class UsuarioUpdate(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=100)] = None
    apellido: Optional[constr(min_length=2, max_length=100)] = None
    cuil: Optional[constr(max_length=13)] = None
    rol: Optional[str] = None
    email: Optional[EmailStr] = None
    id_sucursal: Optional[int] = None
    estado: Optional[bool] = None
    contraseña: Optional[constr(min_length=8)] = None

# Schema para respuesta básica
class UsuarioSimple(UsuarioBase):
    id_usuario: int = Field(
        ...,
        description="ID único del usuario",
        example=1
    )
    estado: bool
    ultimo_acceso: Optional[datetime] = None

    class Config:
        orm_mode = True

# Schema para respuesta completa
class UsuarioCompleta(UsuarioSimple):
    creado_el: datetime
    actualizado_el: datetime
    ventas_count: int = Field(
        0,
        description="Cantidad de ventas realizadas",
        example=50
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_usuario": 1,
                "nombre": "Juan",
                "apellido": "Pérez",
                "cuil": "20-12345678-9",
                "rol": "Vendedor",
                "email": "juan.perez@ferreteria.com",
                "id_sucursal": 1,
                "estado": True,
                "ultimo_acceso": "2024-01-20T15:30:00",
                "creado_el": "2024-01-01T10:00:00",
                "actualizado_el": "2024-01-20T15:30:00",
                "ventas_count": 50
            }
        }
