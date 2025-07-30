from pydantic import BaseModel, Field, constr, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str = Field(..., description="Token de acceso JWT")
    token_type: str = Field(..., description="Tipo de token (siempre 'bearer')")
    user: dict = Field(..., description="Información básica del usuario")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "email": "usuario@email.com",
                    "nombre": "Juan",
                    "apellido": "González",
                    "rol": "admin",
                    "sucursal_id": 1
                }
            }
        }

class TokenData(BaseModel):
    email: Optional[str] = None

class UsuarioBase(BaseModel):
    Nombre: constr(min_length=1, max_length=100) = Field(..., description="Nombre del usuario", alias="nombre")
    Apellido: constr(min_length=1, max_length=100) = Field(..., description="Apellido del usuario", alias="apellido")
    CUIL: Optional[constr(min_length=11, max_length=13)] = Field(None, description="CUIL del usuario", alias="cuil")
    Rol: constr(min_length=1, max_length=50) = Field(..., description="Rol del usuario", alias="rol")
    Email: EmailStr = Field(..., description="Email del usuario", alias="email")
    ID_Sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada", alias="id_sucursal")

    class Config:
        from_attributes = True
        populate_by_name = True

class UsuarioCreate(UsuarioBase):
    Contraseña: constr(min_length=6) = Field(..., description="Contraseña del usuario", alias="contraseña")

class UsuarioUpdate(BaseModel):
    Nombre: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Nombre del usuario", alias="nombre")
    Apellido: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Apellido del usuario", alias="apellido")
    CUIL: Optional[constr(min_length=11, max_length=13)] = Field(None, description="CUIL del usuario", alias="cuil")
    Rol: Optional[constr(min_length=1, max_length=50)] = Field(None, description="Rol del usuario", alias="rol")
    Email: Optional[EmailStr] = Field(None, description="Email del usuario", alias="email")
    Contraseña: Optional[constr(min_length=6)] = Field(None, description="Nueva contraseña del usuario", alias="contraseña")
    ID_Sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada", alias="id_sucursal")
    Estado: Optional[bool] = Field(None, description="Estado del usuario", alias="estado")

    class Config:
        from_attributes = True
        populate_by_name = True

class UsuarioSimple(BaseModel):
    ID_Usuario: int = Field(..., description="ID único del usuario", alias="id_usuario")
    Nombre: str = Field(..., description="Nombre del usuario", alias="nombre")
    Apellido: str = Field(..., description="Apellido del usuario", alias="apellido")
    Email: str = Field(..., description="Email del usuario", alias="email")
    Rol: str = Field(..., description="Rol del usuario", alias="rol")
    Estado: bool = Field(..., description="Estado del usuario", alias="estado")
    sucursal: Optional[str] = Field(None, description="Nombre de la sucursal asignada")

    class Config:
        from_attributes = True
        populate_by_name = True

class UsuarioCompleta(UsuarioSimple):
    CUIL: Optional[str] = Field(None, description="CUIL del usuario", alias="cuil")
    ID_Sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada", alias="id_sucursal")
    Ultimo_Acceso: Optional[datetime] = Field(None, description="Fecha y hora del último acceso", alias="ultimo_acceso")
    Creado_el: datetime = Field(..., description="Fecha y hora de creación", alias="creado_el")
    Actualizado_el: datetime = Field(..., description="Fecha y hora de última actualización", alias="actualizado_el")

    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id_usuario": 1,
                "nombre": "Juan",
                "apellido": "González",
                "email": "juan.gonzalez@ferreteria.com",
                "rol": "admin",
                "estado": True,
                "sucursal": "Sucursal Central",
                "cuil": "20-12345678-9",
                "id_sucursal": 1,
                "ultimo_acceso": "2024-01-01T10:00:00",
                "creado_el": "2024-01-01T00:00:00",
                "actualizado_el": "2024-01-01T00:00:00"
            }
        }

class UsuarioList(BaseModel):
    total_registros: int = Field(..., description="Total de registros encontrados")
    pagina_actual: int = Field(..., description="Número de página actual")
    total_paginas: int = Field(..., description="Total de páginas disponibles")
    usuarios: List[UsuarioSimple] = Field(..., description="Lista de usuarios")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_registros": 100,
                "pagina_actual": 1,
                "total_paginas": 10,
                "usuarios": [
                    {
                        "id_usuario": 1,
                        "nombre": "Juan",
                        "apellido": "González",
                        "email": "juan.gonzalez@ferreteria.com",
                        "rol": "admin",
                        "estado": True,
                        "sucursal": "Sucursal Central"
                    }
                ]
            }
        }
