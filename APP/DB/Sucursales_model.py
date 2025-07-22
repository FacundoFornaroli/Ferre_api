from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Sucursales(Base):
    __tablename__ = "Sucursales"
    ID_Sucursal = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False, unique=True)
    Direccion = Column(String(200), nullable=False)
    Telefono = Column(String(40), nullable=True)
    Email = Column(String(120), nullable=True)
    Localidad = Column(String(100), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Codigo_Postal = Column(String(10), nullable=True)
    Horario_Apertura = Column(Time, nullable=True)
    Horario_Cierre = Column(Time, nullable=True)
    Activo = Column(Boolean, default=True, nullable=False)
    