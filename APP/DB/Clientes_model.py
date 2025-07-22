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

    def __repr__(self):
        return f"<Cliente(ID_Cliente={self.ID_Cliente}, Nombre='{self.Nombre}', Apellido='{self.Apellido}', CUIT_CUIL='{self.CUIT_CUIL}', Tipo_Cliente='{self.Tipo_Cliente}', Condicion_IVA='{self.Condicion_IVA}', Direccion='{self.Direccion}', Localidad='{self.Localidad}', Provincia='{self.Provincia}', Codigo_Postal='{self.Codigo_Postal}', Telefono='{self.Telefono}', Telefono_Alternativo='{self.Telefono_Alternativo}', Email='{self.Email}', Fecha_Nacimiento='{self.Fecha_Nacimiento}', Genero='{self.Genero}', Fecha_Alta='{self.Fecha_Alta}', Limite_Credito='{self.Limite_Credito}', Saldo_Actual='{self.Saldo_Actual}', Activo='{self.Activo}', Observaciones='{self.Observaciones}')>"
        
    