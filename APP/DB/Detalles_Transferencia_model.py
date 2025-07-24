from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Detalles_Transferencia(Base):
    __tablename__ = "Detalles_Transferencia"
    ID_Detalle_Transferencia = Column(Integer, primary_key=True, index=True)
    ID_Transferencia = Column(Integer, ForeignKey('Transferencias_Sucursales.ID_Transferencia', ondelete='CASCADE'), 
                            nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Cantidad_Recibida = Column(Integer, nullable=True)

    # Relaciones
    transferencia = relationship("Transferencias_Sucursales", back_populates="detalles")
    producto = relationship("Productos", back_populates="detalles_transferencia")

    __table_args__ = (
        CheckConstraint("Cantidad > 0", name='CK_DetallesTransferencia_Cantidad'),
        CheckConstraint("Cantidad_Recibida IS NULL OR Cantidad_Recibida <= Cantidad", 
                       name='CK_DetallesTransferencia_CantidadRecibida'),
        Index('IX_DetallesTransferencia_Transferencia', 'ID_Transferencia'),
        Index('IX_DetallesTransferencia_Producto', 'ID_Producto')
    )

    def __repr__(self):
        return f"<DetalleTransferencia(ID_Detalle_Transferencia={self.ID_Detalle_Transferencia}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad})>"
    
    

    
    
