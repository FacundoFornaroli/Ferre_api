from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric
from database import Base 
from datetime import datetime

class Detalle_OC(Base):
    __tablename__ = "Detalle_OC"
    ID_Detalle_OC = Column(Integer, primary_key=True, index=True)
    ID_OC = Column(Integer, ForeignKey('Ordenes_Compra.ID_OC', ondelete='CASCADE'), nullable=False)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Costo_Unitario = Column(Numeric(10, 2), nullable=False)
    Descuento_Unitario = Column(Numeric(10, 2), nullable=False, default=0)
    Subtotal = Column(Numeric(10, 2), nullable=False)

    __table_args__ = (
        CheckConstraint('Cantidad > 0', name='CK_DetalleOC_Cantidad'),
        CheckConstraint('Costo_Unitario > 0', name='CK_DetalleOC_Costo'),
    )

    def __repr__(self):
        return f"<DetalleOC(ID_Detalle_OC={self.ID_Detalle_OC}, ID_OC={self.ID_OC}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad})>"
