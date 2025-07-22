from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Date
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Clientes(Base):
    __tablename__ = "Clientes"
    ID_Cliente = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(150), nullable=False)
    Apellido = Column(String(150), nullable=True)
    CUIT_CUIL = Column(String(13), nullable=True, unique=True)
    Tipo_Cliente = Column(String(20), nullable=False, default='Consumidor Final')
    Condicion_IVA = Column(String(50), nullable=True)
    Direccion = Column(String(200), nullable=False)
    Localidad = Column(String(100), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Codigo_Postal = Column(String(10), nullable=True)
    Telefono = Column(String(40), nullable=False)
    Telefono_Alternativo = Column(String(40), nullable=True)
    Email = Column(String(120), nullable=True)
    Fecha_Nacimiento = Column(Date, nullable=True)
    Genero = Column(String(1), nullable=True)
    Fecha_Alta = Column(DateTime, default=datetime.now, nullable=False)
    Limite_Credito = Column(Numeric(10, 2), nullable=False, default=0)
    Saldo_Actual = Column(Numeric(10, 2), nullable=False, default=0)
    Activo = Column(Boolean, default=True, nullable=False)
    Observaciones = Column(Text, nullable=True)

    
    