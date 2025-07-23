from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Detalles_Transferencia(Base):
    __tablename__ = "Detalles_Transferencia"
    ID_Detalle_Transferencia = Column(Integer, primary_key=True, index=True)
    ID_Transferencia = Column(Integer, ForeignKey('Transferencias_Sucursales.ID_Transferencia'), nullable=False, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Cantidad_Recibida = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("Cantidad > 0", name='CK_DetallesTransferencia_Cantidad'),
        Index('IX_DetallesTransferencia_Transferencia', 'ID_Transferencia'),
        Index('IX_DetallesTransferencia_Producto', 'ID_Producto'),
    )

    def __repr__(self):
        return f"<Detalles_Transferencia(ID_Detalle_Transferencia={self.ID_Detalle_Transferencia}, ID_Transferencia={self.ID_Transferencia}, ID_Producto={self.ID_Producto}, Cantidad={self.Cantidad}, Cantidad_Recibida={self.Cantidad_Recibida})>"
    
    # Relaciones
    transferencia = relationship("Transferencias_Sucursales", back_populates="detalles_transferencia")
    producto = relationship("Productos", back_populates="detalles_transferencia")

    

    
    
