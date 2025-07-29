from pydantic import BaseModel, Field, constr, EmailStr
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
    nombre: constr(min_length=1, max_length=100) = Field(..., description="Nombre del usuario")
    apellido: constr(min_length=1, max_length=100) = Field(..., description="Apellido del usuario")
    cuil: Optional[constr(min_length=11, max_length=13)] = Field(None, description="CUIL del usuario")
    rol: constr(min_length=1, max_length=50) = Field(..., description="Rol del usuario")
    email: EmailStr = Field(..., description="Email del usuario")
    id_sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada")

    class Config:
        from_attributes = True

class UsuarioCreate(UsuarioBase):
    contraseña: constr(min_length=6) = Field(..., description="Contraseña del usuario")

class UsuarioUpdate(BaseModel):
    nombre: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Nombre del usuario")
    apellido: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Apellido del usuario")
    cuil: Optional[constr(min_length=11, max_length=13)] = Field(None, description="CUIL del usuario")
    rol: Optional[constr(min_length=1, max_length=50)] = Field(None, description="Rol del usuario")
    email: Optional[EmailStr] = Field(None, description="Email del usuario")
    contraseña: Optional[constr(min_length=6)] = Field(None, description="Nueva contraseña del usuario")
    id_sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada")
    estado: Optional[bool] = Field(None, description="Estado del usuario")

    class Config:
        from_attributes = True

class UsuarioSimple(BaseModel):
    id_usuario: int = Field(..., description="ID único del usuario")
    nombre: str = Field(..., description="Nombre del usuario")
    apellido: str = Field(..., description="Apellido del usuario")
    email: str = Field(..., description="Email del usuario")
    rol: str = Field(..., description="Rol del usuario")
    estado: bool = Field(..., description="Estado del usuario")
    sucursal: Optional[str] = Field(None, description="Nombre de la sucursal asignada")

    class Config:
        from_attributes = True

class UsuarioCompleta(UsuarioSimple):
    cuil: Optional[str] = Field(None, description="CUIL del usuario")
    id_sucursal: Optional[int] = Field(None, description="ID de la sucursal asignada")
    ultimo_acceso: Optional[datetime] = Field(None, description="Fecha y hora del último acceso")
    creado_el: datetime = Field(..., description="Fecha y hora de creación")
    actualizado_el: datetime = Field(..., description="Fecha y hora de última actualización")

    class Config:
        from_attributes = True
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
