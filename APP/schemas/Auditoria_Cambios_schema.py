from pydantic import BaseModel, Field, validator, constr
from typing import Optional, Dict, Any, List
from datetime import datetime

class AuditoriaCambiosBase(BaseModel):
    tabla_afectada: constr(max_length=100) = Field(
        ...,
        description="Nombre de la tabla afectada",
        example="Productos"
    )
    id_registro: int = Field(
        ...,
        description="ID del registro afectado",
        example=1
    )
    tipo_operacion: constr(max_length=20) = Field(
        ...,
        description="Tipo de operación realizada",
        example="UPDATE"
    )
    id_usuario: int = Field(
        ...,
        description="ID del usuario que realizó la operación",
        example=1
    )
    datos_anteriores: Optional[str] = Field(
        None,
        description="Datos antes del cambio",
        example="Precio anterior: $4500.00"
    )
    datos_nuevos: Optional[str] = Field(
        None,
        description="Datos después del cambio",
        example="Precio nuevo: $4800.00"
    )
    ip_cliente: Optional[constr(max_length=45)] = Field(
        None,
        description="IP del cliente",
        example="192.168.1.100"
    )

    @validator('tipo_operacion')
    def validar_tipo_operacion(cls, v):
        tipos_validos = ['INSERT', 'UPDATE', 'DELETE']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de operación debe ser uno de: {", ".join(tipos_validos)}')
        return v

class AuditoriaCambiosCreate(AuditoriaCambiosBase):
    pass

class AuditoriaCambiosSimple(AuditoriaCambiosBase):
    id_auditoria: int = Field(..., description="ID único del registro de auditoría")
    fecha_operacion: datetime
    usuario_nombre: str = Field(..., example="Juan Pérez")

    class Config:
        from_attributes = True

class AuditoriaCambiosCompleta(AuditoriaCambiosSimple):
    # Información adicional del usuario
    usuario_info: dict = Field(
        ...,
        example={
            "nombre": "Juan Pérez",
            "rol": "Administrador",
            "sucursal": "Sucursal Centro"
        }
    )
    
    # Información del registro afectado
    registro_info: dict = Field(
        ...,
        example={
            "tabla": "Productos",
            "id": 1,
            "nombre": "Martillo Profesional",
            "identificador": "MART-001"
        }
    )
    
    # Cambios detallados
    cambios_detallados: Dict[str, dict] = Field(
        ...,
        description="Detalle de los cambios por campo",
        example={
            "precio": {
                "anterior": 4500.00,
                "nuevo": 4800.00,
                "diferencia": 300.00,
                "porcentaje_cambio": 6.67
            },
            "stock_minimo": {
                "anterior": 5,
                "nuevo": 10,
                "diferencia": 5,
                "porcentaje_cambio": 100.00
            }
        }
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_auditoria": 1,
                "fecha_operacion": "2024-01-15T10:30:00",
                "tabla_afectada": "Productos",
                "id_registro": 1,
                "tipo_operacion": "UPDATE",
                "id_usuario": 1,
                "usuario_nombre": "Juan Pérez",
                "usuario_info": {
                    "nombre": "Juan Pérez",
                    "rol": "Administrador",
                    "sucursal": "Sucursal Centro"
                },
                "registro_info": {
                    "tabla": "Productos",
                    "id": 1,
                    "nombre": "Martillo Profesional",
                    "identificador": "MART-001"
                },
                "datos_anteriores": "Precio anterior: $4500.00, Stock mínimo: 5",
                "datos_nuevos": "Precio nuevo: $4800.00, Stock mínimo: 10",
                "cambios_detallados": {
                    "precio": {
                        "anterior": 4500.00,
                        "nuevo": 4800.00,
                        "diferencia": 300.00,
                        "porcentaje_cambio": 6.67
                    },
                    "stock_minimo": {
                        "anterior": 5,
                        "nuevo": 10,
                        "diferencia": 5,
                        "porcentaje_cambio": 100.00
                    }
                },
                "ip_cliente": "192.168.1.100"
            }
        }

class AuditoriaCambiosList(BaseModel):
    total_registros: int
    pagina_actual: int
    total_paginas: int
    registros: List[AuditoriaCambiosSimple]

    class Config:
        from_attributes = True

# Schema para estadísticas de auditoría
class EstadisticasAuditoria(BaseModel):
    periodo: str = Field(..., example="2024-01")
    total_operaciones: int
    operaciones_por_tipo: dict = Field(
        ...,
        example={
            "INSERT": 150,
            "UPDATE": 300,
            "DELETE": 50
        }
    )
    operaciones_por_tabla: List[dict] = Field(
        ...,
        example=[
            {
                "tabla": "Productos",
                "total": 200,
                "inserts": 50,
                "updates": 130,
                "deletes": 20
            }
        ]
    )
    usuarios_mas_activos: List[dict] = Field(
        ...,
        example=[
            {
                "usuario": "Juan Pérez",
                "operaciones": 150,
                "tablas_principales": ["Productos", "Inventario"]
            }
        ]
    )
    horas_pico: dict = Field(
        ...,
        example={
            "hora_mas_activa": "10:00",
            "operaciones_por_hora": {
                "09:00": 50,
                "10:00": 80,
                "11:00": 45
            }
        }
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "periodo": "2024-01",
                "total_operaciones": 500,
                "operaciones_por_tipo": {
                    "INSERT": 150,
                    "UPDATE": 300,
                    "DELETE": 50
                },
                "operaciones_por_tabla": [
                    {
                        "tabla": "Productos",
                        "total": 200,
                        "inserts": 50,
                        "updates": 130,
                        "deletes": 20
                    }
                ],
                "usuarios_mas_activos": [
                    {
                        "usuario": "Juan Pérez",
                        "operaciones": 150,
                        "tablas_principales": ["Productos", "Inventario"]
                    }
                ],
                "horas_pico": {
                    "hora_mas_activa": "10:00",
                    "operaciones_por_hora": {
                        "09:00": 50,
                        "10:00": 80,
                        "11:00": 45
                    }
                }
            }
        }

# Schema para búsqueda de auditoría
class BusquedaAuditoria(BaseModel):
    fecha_inicio: datetime
    fecha_fin: datetime
    tablas: Optional[List[str]] = None
    tipos_operacion: Optional[List[str]] = None
    usuarios: Optional[List[int]] = None
    campos_modificados: Optional[List[str]] = None
    valor_busqueda: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "fecha_inicio": "2024-01-01T00:00:00",
                "fecha_fin": "2024-01-31T23:59:59",
                "tablas": ["Productos", "Inventario"],
                "tipos_operacion": ["UPDATE"],
                "usuarios": [1, 2],
                "campos_modificados": ["precio", "stock_minimo"],
                "valor_busqueda": "4500.00"
            }
        }
