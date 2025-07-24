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
    Tipo_Descuento = Column(String(20), nullable=False, index=True)
    Fecha_Inicio = Column(Date, nullable=False, index=True)
    Fecha_Fin = Column(Date, nullable=False, index=True)
    Cantidad_Minima = Column(Integer, nullable=True)
    Cantidad_Maxima = Column(Integer, nullable=True)
    Activo = Column(Boolean, nullable=False, default=True, index=True)

    # Relaciones
    productos_descuentos = relationship("Productos_Descuentos", back_populates="descuento", cascade="all, delete-orphan")
    productos = relationship("Productos", secondary="Productos_Descuentos", back_populates="descuentos")

    __table_args__ = (
        CheckConstraint("Tipo_Descuento IN ('Porcentaje', 'Monto Fijo')", 
                       name='CK_Descuentos_Tipo'),
        CheckConstraint("Porcentaje >= 0 AND Porcentaje <= 100", 
                       name='CK_Descuentos_Porcentaje'),
        CheckConstraint("Fecha_Fin >= Fecha_Inicio", 
                       name='CK_Descuentos_Fechas'),
        CheckConstraint("(Cantidad_Maxima IS NULL) OR (Cantidad_Maxima >= Cantidad_Minima)", 
                       name='CK_Descuentos_Cantidades'),
        Index('IX_Descuentos_Tipo', 'Tipo_Descuento'),
        Index('IX_Descuentos_FechaInicio', 'Fecha_Inicio'),
        Index('IX_Descuentos_FechaFin', 'Fecha_Fin'),
        Index('IX_Descuentos_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Descuento(ID_Descuento={self.ID_Descuento}, Nombre='{self.Nombre}', Tipo='{self.Tipo_Descuento}')>"
    