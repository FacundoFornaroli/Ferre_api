from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Detalle_OC(Base):
    __tablename__ = "Detalle_OC"
    ID_Detalle_OC = Column(Integer, primary_key=True, index=True)
    ID_OC = Column(Integer, ForeignKey('Ordenes_Compra.ID_OC', ondelete='CASCADE'), nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Costo_Unitario = Column(Numeric(10, 2), nullable=False)
    Descuento_Unitario = Column(Numeric(10, 2), nullable=False, default=0)
    Subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    orden = relationship("Ordenes_Compra", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_oc")

    __table_args__ = (
        CheckConstraint('Cantidad > 0', name='CK_DetalleOC_Cantidad'),
        CheckConstraint('Costo_Unitario > 0', name='CK_DetalleOC_Costo'),
        Index('IX_DetalleOC_Orden', 'ID_OC'),
        Index('IX_DetalleOC_Producto', 'ID_Producto')
    )

    def __repr__(self):
        return f"<DetalleOC(ID_Detalle_OC={self.ID_Detalle_OC}, ID_OC={self.ID_OC}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad})>"
        