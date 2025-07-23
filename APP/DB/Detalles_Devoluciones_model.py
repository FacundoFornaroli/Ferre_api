from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Detalles_Devoluciones(Base):
    __tablename__ = "Detalles_Devoluciones"
    ID_Detalle_Devolucion = Column(Integer, primary_key=True, index=True)
    ID_Devolucion = Column(Integer, ForeignKey('Devoluciones.ID_Devolucion'), nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Motivo_Especifico = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("Cantidad > 0", name='CK_DetallesDevolucion_Cantidad'),
        Index('IX_DetallesDevolucion_Devolucion', 'ID_Devolucion'),
        Index('IX_DetallesDevolucion_Producto', 'ID_Producto'),
    )

    def __repr__(self):
        return f"<Detalles_Devoluciones(ID_Detalle_Devolucion={self.ID_Detalle_Devolucion}, ID_Devolucion={self.ID_Devolucion}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad}, Motivo_Especifico={self.Motivo_Especifico})>"
    
    # Relaciones
    devolucion = relationship("Devoluciones", back_populates="detalles_devolucion")
    producto = relationship("Productos", back_populates="detalles_devolucion")

