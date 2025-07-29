from pydantic import BaseModel, Field, constr, EmailStr
from typing import Optional, List
from datetime import datetime

class SucursalBase(BaseModel):
    nombre: constr(min_length=1, max_length=100) = Field(..., description="Nombre de la sucursal")
    direccion: constr(min_length=1, max_length=200) = Field(..., description="Dirección de la sucursal")
    telefono: Optional[constr(max_length=40)] = Field(None, description="Teléfono de la sucursal")
    email: Optional[EmailStr] = Field(None, description="Email de la sucursal")
    localidad: constr(min_length=1, max_length=100) = Field(..., description="Localidad de la sucursal")
    provincia: constr(min_length=1, max_length=50) = Field(..., description="Provincia de la sucursal")
    codigo_postal: Optional[constr(max_length=10)] = Field(None, description="Código postal de la sucursal")
    horario_apertura: Optional[str] = Field(None, description="Horario de apertura (formato HH:MM)")
    horario_cierre: Optional[str] = Field(None, description="Horario de cierre (formato HH:MM)")
    activo: bool = Field(True, description="Estado de la sucursal")

    class Config:
        from_attributes = True

class SucursalCreate(SucursalBase):
    pass

class SucursalUpdate(BaseModel):
    nombre: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Nombre de la sucursal")
    direccion: Optional[constr(min_length=1, max_length=200)] = Field(None, description="Dirección de la sucursal")
    telefono: Optional[constr(max_length=40)] = Field(None, description="Teléfono de la sucursal")
    email: Optional[EmailStr] = Field(None, description="Email de la sucursal")
    localidad: Optional[constr(min_length=1, max_length=100)] = Field(None, description="Localidad de la sucursal")
    provincia: Optional[constr(min_length=1, max_length=50)] = Field(None, description="Provincia de la sucursal")
    codigo_postal: Optional[constr(max_length=10)] = Field(None, description="Código postal de la sucursal")
    horario_apertura: Optional[str] = Field(None, description="Horario de apertura (formato HH:MM)")
    horario_cierre: Optional[str] = Field(None, description="Horario de cierre (formato HH:MM)")
    activo: Optional[bool] = Field(None, description="Estado de la sucursal")

    class Config:
        from_attributes = True

class SucursalSimple(BaseModel):
    id_sucursal: int = Field(..., description="ID único de la sucursal")
    nombre: str = Field(..., description="Nombre de la sucursal")
    direccion: str = Field(..., description="Dirección de la sucursal")
    telefono: Optional[str] = Field(None, description="Teléfono de la sucursal")
    email: Optional[str] = Field(None, description="Email de la sucursal")
    localidad: str = Field(..., description="Localidad de la sucursal")
    provincia: str = Field(..., description="Provincia de la sucursal")
    codigo_postal: Optional[str] = Field(None, description="Código postal de la sucursal")
    horario_apertura: Optional[str] = Field(None, description="Horario de apertura (formato HH:MM)")
    horario_cierre: Optional[str] = Field(None, description="Horario de cierre (formato HH:MM)")
    activo: bool = Field(..., description="Estado de la sucursal")
    usuarios_count: int = Field(0, description="Cantidad de usuarios activos en la sucursal")
    productos_count: int = Field(0, description="Cantidad de productos activos en la sucursal")
    ventas_count: int = Field(0, description="Cantidad de ventas realizadas en la sucursal")

    class Config:
        from_attributes = True

class SucursalCompleta(SucursalSimple):
    fecha_creacion: datetime = Field(..., description="Fecha de creación de la sucursal")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_sucursal": 1,
                "nombre": "Sucursal Central",
                "direccion": "Av. Principal 123",
                "telefono": "+54 11 1234-5678",
                "email": "central@ferreteria.com",
                "localidad": "Ciudad Autónoma de Buenos Aires",
                "provincia": "Buenos Aires",
                "codigo_postal": "C1001",
                "horario_apertura": "08:00",
                "horario_cierre": "18:00",
                "activo": True,
                "fecha_creacion": "2024-01-01T00:00:00",
                "usuarios_count": 10,
                "productos_count": 1000,
                "ventas_count": 500
            }
        }

class SucursalList(BaseModel):
    total_registros: int = Field(..., description="Total de registros encontrados")
    pagina_actual: int = Field(..., description="Número de página actual")
    total_paginas: int = Field(..., description="Total de páginas disponibles")
    sucursales: List[SucursalSimple] = Field(..., description="Lista de sucursales")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_registros": 100,
                "pagina_actual": 1,
                "total_paginas": 10,
                "sucursales": [
                    {
                        "id_sucursal": 1,
                        "nombre": "Sucursal Central",
                        "direccion": "Av. Principal 123",
                        "telefono": "+54 11 1234-5678",
                        "email": "central@ferreteria.com",
                        "localidad": "Ciudad Autónoma de Buenos Aires",
                        "provincia": "Buenos Aires",
                        "codigo_postal": "C1001",
                        "horario_apertura": "08:00",
                        "horario_cierre": "18:00",
                        "activo": True,
                        "usuarios_count": 10,
                        "productos_count": 1000,
                        "ventas_count": 500
                    }
                ]
            }
        }

class SucursalEstadisticas(BaseModel):
    total_sucursales: int = Field(..., description="Total de sucursales")
    sucursales_activas: int = Field(..., description="Total de sucursales activas")
    sucursales_por_provincia: List[dict] = Field(..., description="Distribución de sucursales por provincia")
    sucursales_mas_ventas: List[dict] = Field(..., description="Top 5 sucursales con más ventas")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "total_sucursales": 100,
                "sucursales_activas": 95,
                "sucursales_por_provincia": [
                    {
                        "provincia": "Buenos Aires",
                        "total_sucursales": 50,
                        "sucursales_activas": 48
                    }
                ],
                "sucursales_mas_ventas": [
                    {
                        "id": 1,
                        "nombre": "Sucursal Central",
                        "localidad": "CABA",
                        "provincia": "Buenos Aires",
                        "total_ventas": 1000,
                        "monto_total": 5000000.00
                    }
                ]
            }
        }
