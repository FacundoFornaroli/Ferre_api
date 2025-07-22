from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Date, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Descuentos(Base):
    __tablename__ = "Descuentos"
    ID_Descuento = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(Text, nullable=True)
    Porcentaje = Column(Numeric(5, 2), nullable=False)
    Monto_Fijo = Column(Numeric(10, 2), nullable=True)
    Tipo_Descuento = Column(String(20), nullable=False)
    Fecha_Inicio = Column(Date, nullable=False)
    Fecha_Fin = Column(Date, nullable=False)
    Cantidad_Minima = Column(Integer, nullable=True)
    Cantidad_Maxima = Column(Integer, nullable=True)
    Activo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("Tipo_Descuento IN ('Porcentaje', 'Monto Fijo')", name='CK_Descuentos_Tipo'),
        Index('IX_Descuentos_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Descuentos(ID_Descuento={self.ID_Descuento}, Nombre={self.Nombre}, Descripcion={self.Descripcion}, Porcentaje={self.Porcentaje}, Monto_Fijo={self.Monto_Fijo}, Tipo_Descuento={self.Tipo_Descuento}, Fecha_Inicio={self.Fecha_Inicio}, Fecha_Fin={self.Fecha_Fin}, Cantidad_Minima={self.Cantidad_Minima}, Cantidad_Maxima={self.Cantidad_Maxima}, Activo={self.Activo})>"
    