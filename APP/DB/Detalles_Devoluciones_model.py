from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Detalles_Devolucion(Base):
    __tablename__ = "Detalles_Devolucion"
    ID_Detalle_Devolucion = Column(Integer, primary_key=True, index=True)
    ID_Devolucion = Column(Integer, ForeignKey('Devoluciones.ID_Devolucion', ondelete='CASCADE'), nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Motivo_Especifico = Column(String(200), nullable=True)

    # Relaciones
    devolucion = relationship("Devoluciones", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_devolucion")

    __table_args__ = (
        CheckConstraint("Cantidad > 0", name='CK_DetallesDevolucion_Cantidad'),
        Index('IX_DetallesDevolucion_Devolucion', 'ID_Devolucion'),
        Index('IX_DetallesDevolucion_Producto', 'ID_Producto')
    )

    def __repr__(self):
        return f"<DetalleDevolucion(ID_Detalle_Devolucion={self.ID_Detalle_Devolucion}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad})>"

