from pydantic import BaseModel, Field, constr, validator, EmailStr, condecimal
from typing import Optional, List
from datetime import datetime, date

# Schema Base
class ClienteBase(BaseModel):
    nombre: constr(min_length=2, max_length=150, strip_whitespace=True) = Field(
        ...,
        description="Nombre del cliente",
        example="Juan Carlos"
    )
    apellido: Optional[constr(max_length=150, strip_whitespace=True)] = Field(
        None,
        description="Apellido del cliente",
        example="Pérez"
    )
    cuit_cuil: Optional[constr(max_length=13, strip_whitespace=True)] = Field(
        None,
        description="CUIT/CUIL del cliente",
        example="20-12345678-9"
    )
    tipo_cliente: constr(max_length=20) = Field(
        "Consumidor Final",
        description="Tipo de cliente",
        example="Consumidor Final"
    )
    condicion_iva: Optional[constr(max_length=50)] = Field(
        None,
        description="Condición frente al IVA",
        example="Responsable Inscripto"
    )
    direccion: constr(min_length=5, max_length=200, strip_whitespace=True) = Field(
        ...,
        description="Dirección del cliente",
        example="Av. Siempreviva 742"
    )
    localidad: constr(min_length=2, max_length=100, strip_whitespace=True) = Field(
        ...,
        description="Localidad del cliente",
        example="Springfield"
    )
    provincia: constr(min_length=2, max_length=50, strip_whitespace=True) = Field(
        ...,
        description="Provincia del cliente",
        example="Buenos Aires"
    )
    codigo_postal: Optional[constr(max_length=10, strip_whitespace=True)] = Field(
        None,
        description="Código postal",
        example="1234"
    )
    telefono: constr(max_length=40, strip_whitespace=True) = Field(
        ...,
        description="Teléfono principal",
        example="351-1234567"
    )
    telefono_alternativo: Optional[constr(max_length=40)] = Field(
        None,
        description="Teléfono alternativo",
        example="351-7654321"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Correo electrónico",
        example="juan.perez@email.com"
    )
    fecha_nacimiento: Optional[date] = Field(
        None,
        description="Fecha de nacimiento",
        example="1980-01-01"
    )
    genero: Optional[constr(max_length=1)] = Field(
        None,
        description="Género (M/F/O)",
        example="M"
    )
    limite_credito: condecimal(ge=0, decimal_places=2) = Field(
        0,
        description="Límite de crédito",
        example=50000.00
    )
    observaciones: Optional[str] = Field(
        None,
        description="Observaciones generales",
        example="Cliente preferencial"
    )

    @validator('cuit_cuil')
    def validar_cuit_cuil(cls, v):
        if v:
            v = v.replace('-', '').replace(' ', '')
            if not v.isdigit() or len(v) != 11:
                raise ValueError('CUIT/CUIL inválido')
            return f"{v[:2]}-{v[2:10]}-{v[10]}"
        return v

    @validator('tipo_cliente')
    def validar_tipo_cliente(cls, v):
        tipos_validos = ['Consumidor Final', 'Responsable Inscripto', 'Monotributista']
        if v not in tipos_validos:
            raise ValueError(f'Tipo de cliente debe ser uno de: {", ".join(tipos_validos)}')
        return v

    @validator('genero')
    def validar_genero(cls, v):
        if v and v not in ['M', 'F', 'O']:
            raise ValueError('Género debe ser M, F u O')
        return v

# Schema para Crear
class ClienteCreate(ClienteBase):
    pass

# Schema para Actualizar
class ClienteUpdate(BaseModel):
    nombre: Optional[constr(min_length=2, max_length=150)] = None
    apellido: Optional[constr(max_length=150)] = None
    cuit_cuil: Optional[constr(max_length=13)] = None
    tipo_cliente: Optional[str] = None
    condicion_iva: Optional[str] = None
    direccion: Optional[constr(min_length=5, max_length=200)] = None
    localidad: Optional[constr(max_length=100)] = None
    provincia: Optional[constr(max_length=50)] = None
    codigo_postal: Optional[constr(max_length=10)] = None
    telefono: Optional[constr(max_length=40)] = None
    telefono_alternativo: Optional[constr(max_length=40)] = None
    email: Optional[EmailStr] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[str] = None
    limite_credito: Optional[condecimal(ge=0, decimal_places=2)] = None
    activo: Optional[bool] = None
    observaciones: Optional[str] = None

# Schema para respuesta básica
class ClienteSimple(ClienteBase):
    id_cliente: int = Field(..., description="ID único del cliente")
    activo: bool
    saldo_actual: condecimal(decimal_places=2) = Field(
        0,
        description="Saldo actual del cliente",
        example=0.00
    )

    class Config:
        orm_mode = True

# Schema para respuesta completa
class ClienteCompleta(ClienteSimple):
    fecha_alta: datetime
    compras_count: int = Field(
        0,
        description="Cantidad total de compras realizadas",
        example=10
    )
    ultima_compra: Optional[datetime] = Field(
        None,
        description="Fecha de la última compra"
    )
    total_comprado: condecimal(decimal_places=2) = Field(
        0,
        description="Monto total histórico de compras",
        example=150000.00
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id_cliente": 1,
                "nombre": "Juan Carlos",
                "apellido": "Pérez",
                "cuit_cuil": "20-12345678-9",
                "tipo_cliente": "Consumidor Final",
                "condicion_iva": "Responsable Inscripto",
                "direccion": "Av. Siempreviva 742",
                "localidad": "Springfield",
                "provincia": "Buenos Aires",
                "codigo_postal": "1234",
                "telefono": "351-1234567",
                "telefono_alternativo": "351-7654321",
                "email": "juan.perez@email.com",
                "fecha_nacimiento": "1980-01-01",
                "genero": "M",
                "limite_credito": 50000.00,
                "saldo_actual": 1500.00,
                "activo": True,
                "fecha_alta": "2024-01-01T10:00:00",
                "compras_count": 10,
                "ultima_compra": "2024-01-20T15:30:00",
                "total_comprado": 150000.00,
                "observaciones": "Cliente preferencial"
            }
        }
