from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Detalles_Factura_Venta(Base):
    __tablename__ = "Detalles_Factura_Venta"
    
    ID_Detalle = Column(Integer, primary_key=True, index=True)
    ID_Factura_Venta = Column(Integer, ForeignKey('Facturas_Venta.ID_Factura_Venta', ondelete='CASCADE'), nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Precio_Unitario = Column(Numeric(10,2), nullable=False)
    Descuento_Unitario = Column(Numeric(10,2), nullable=False, default=0)
    Subtotal = Column(Numeric(10,2), nullable=False)

    # Relaciones
    factura = relationship("Facturas_Venta", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_factura")

    __table_args__ = (
        CheckConstraint('Cantidad > 0', name='CK_DetallesFactura_Cantidad'),
        CheckConstraint('Precio_Unitario > 0', name='CK_DetallesFactura_Precio'),
        Index('IX_DetallesFactura_Factura', 'ID_Factura_Venta'),
        Index('IX_DetallesFactura_Producto', 'ID_Producto')
    )

    def __repr__(self):
        return f"<DetalleFactura(ID_Detalle={self.ID_Detalle}, ID_Factura_Venta={self.ID_Factura_Venta}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad})>"
        