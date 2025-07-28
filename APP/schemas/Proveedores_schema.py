from pydantic import BaseModel, Field, constr, validator, EmailStr
from typing import Optional, List
from datetime import datetime

# Schema Base
class ProveedorBase(BaseModel):
    nombre: constr(min_length=2, max_length=150, strip_whitespace=True) = Field(
        ...,
        description="Nombre o razón social del proveedor",
        example="Stanley Black & Decker Argentina S.A."
    )
    cuit: Optional[constr(max_length=13, strip_whitespace=True)] = Field(
        None,
        description="CUIT del proveedor",
        example="30-12345678-9"
    )
    condicion_iva: Optional[constr(max_length=50)] = Field(
        None,
        description="Condición frente al IVA",
        example="IVA Responsable Inscripto"
    )
    direccion: constr(min_length=5, max_length=200, strip_whitespace=True) = Field(
        ...,
        description="Dirección del proveedor",
        example="Av. del Libertador 1234"
    )
    localidad: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Localidad del proveedor",
        example="Buenos Aires"
    )
    provincia: constr(min_length=2, max_length=50, strip_whitespace=True) = Field(
        ...,
        description="Provincia del proveedor",
        example="Buenos Aires"
    )
    codigo_postal: Optional[constr(max_length=10, strip_whitespace=True)] = Field(
        None,
        description="Código postal",
        example="1425"
    )
    telefono: constr(max_length=40, strip_whitespace=True) = Field(
        ...,
        description="Teléfono principal",
        example="011-4321-7000"
    )
    telefono_alternativo: Optional[constr(max_length=40)] = Field(
        None,
        description="Teléfono alternativo",
        example="011-4321-7001"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Correo electrónico",
        example="ventas@stanley.com.ar"
    )
    contacto_persona: Optional[constr(max_length=100)] = Field(
        None,
        description="Nombre de la persona de contacto",
        example="Juan Pérez"
    )
    plazo_entrega: Optional[int] = Field(
        None,
        description="Plazo de entrega en días",
        example=7,
        ge=0
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones generales"
    )

    @validator('cuit')
    def validar_cuit(cls, v):
        if v:
            v = v.replace('-', '').replace(' ', '')
            if not v.isdigit() or len(v) != 11:
                raise ValueError('CUIT inválido')
            return f"{v[:2]}-{v[2:10]}-{v[10]}"
        return v

# Schema para Crear
class ProveedorCreate(ProveedorBase):
    pass

# Schema para Actualizar
class ProveedorUpdate(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=150)] = None
    cuit: Optional[constr(max_length=13)] = None
    condicion_iva: Optional[str] = None
    direccion: Optional[constr(min_length=5, max_length=200)] = None
    localidad: Optional[constr(max_length=100)] = None
    provincia: Optional[constr(max_length=50)] = None
    codigo_postal: Optional[constr(max_length=10)] = None
    telefono: Optional[constr(max_length=40)] = None
    telefono_alternativo: Optional[constr(max_length=40)] = None
    email: Optional[EmailStr] = None
    contacto_persona: Optional[constr(max_length=100)] = None
    plazo_entrega: Optional[int] = None
    activo: Optional[bool] = None
    observaciones: Optional[str] = None

# Schema para respuesta básica
class ProveedorSimple(ProveedorBase):
    id_proveedor: int = Field(..., description="ID único del proveedor")
    activo: bool
    ordenes_pendientes: int = Field(
        0,
        description="Cantidad de órdenes de compra pendientes",
        example=3
    )

    class Config:
        from_attributes = True

# Schema para respuesta completa
class ProveedorCompleta(ProveedorSimple):
    fecha_creacion: datetime
    total_ordenes: int = Field(
        0,
        description="Total de órdenes de compra realizadas",
        example=25
    )
    ultima_orden: Optional[datetime] = Field(
        None,
        description="Fecha de la última orden de compra"
    )
    monto_total_compras: float = Field(
        0.0,
        description="Monto total histórico de compras",
        example=1500000.00
    )
    promedio_tiempo_entrega: float = Field(
        0.0,
        description="Promedio de días de entrega real",
        example=7.5
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_proveedor": 1,
                "nombre": "Stanley Black & Decker Argentina S.A.",
                "cuit": "30-12345678-9",
                "condicion_iva": "IVA Responsable Inscripto",
                "direccion": "Av. del Libertador 1234",
                "localidad": "Buenos Aires",
                "provincia": "Buenos Aires",
                "codigo_postal": "1425",
                "telefono": "011-4321-7000",
                "telefono_alternativo": "011-4321-7001",
                "email": "ventas@stanley.com.ar",
                "contacto_persona": "Juan Pérez",
                "plazo_entrega": 7,
                "activo": True,
                "ordenes_pendientes": 3,
                "fecha_creacion": "2024-01-01T10:00:00",
                "total_ordenes": 25,
                "ultima_orden": "2024-01-20T15:30:00",
                "monto_total_compras": 1500000.00,
                "promedio_tiempo_entrega": 7.5,
                "observaciones": "Proveedor principal de herramientas"
            }
        }

# Schema para lista paginada de proveedores
class ProveedorList(BaseModel):
    total: int = Field(..., description="Total de registros")
    pagina: int = Field(..., description="Página actual")
    paginas: int = Field(..., description="Total de páginas")
    items: List[ProveedorSimple]

    class Config:
        from_attributes = True
