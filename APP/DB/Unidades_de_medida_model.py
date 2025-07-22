from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime


class Unidades_de_medida(Base):
    __tablename__ = "Unidades_de_medida"
    ID_Unidad_de_medida = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(50), nullable=False, unique=True)
    Abreviatura = Column(String(10), nullable=False, unique=True)
    Activo = Column(Boolean, default=True, nullable=False)

CheckConstraint(Nombre == Abreviatura, name='check_nombre_abreviatura')
