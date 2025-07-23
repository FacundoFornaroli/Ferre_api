from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index, UniqueConstraint
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Productos_Descuentos(Base):
    __tablename__ = "Productos_Descuentos"
    ID_Producto_Descuento = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    ID_Descuento = Column(Integer, ForeignKey('Descuentos.ID_Descuento'), nullable=False, index=True)

    __table_args__ = (
        UniqueConstraint('ID_Producto', 'ID_Descuento', name='UQ_Producto_Descuento'),
        Index('IX_ProductosDescuentos_Producto', 'ID_Producto'),
        Index('IX_ProductosDescuentos_Descuento', 'ID_Descuento'),
    )

    def __repr__(self):
        return f"<Productos_Descuentos(ID_Producto_Descuento={self.ID_Producto_Descuento}, ID_Producto={self.ID_Producto}, ID_Descuento={self.ID_Descuento})>"
    
    # Relaciones
    producto = relationship("Productos", back_populates="productos_descuentos")
    descuento = relationship("Descuentos", back_populates="productos_descuentos")

