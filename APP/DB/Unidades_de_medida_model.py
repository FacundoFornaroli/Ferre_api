from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime


class Unidades_de_medida(Base):
    __tablename__ = "Unidades_de_medida"
    ID_Unidad_de_medida = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(50), nullable=False, unique=True)
    Abreviatura = Column(String(10), nullable=False, unique=True)
    Activo = Column(Boolean, default=True, nullable=False, index=True)

    # Relaciones
    productos = relationship("Productos", back_populates="unidad_medida")

    __table_args__ = (
        CheckConstraint('Nombre != Abreviatura', name='check_nombre_abreviatura'),
        Index('IX_UnidadesMedida_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Unidad_de_medida(ID_Unidad_de_medida={self.ID_Unidad_de_medida}, Nombre='{self.Nombre}', Abreviatura='{self.Abreviatura}')>"
