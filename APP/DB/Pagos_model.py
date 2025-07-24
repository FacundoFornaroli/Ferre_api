from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Pagos(Base):
    __tablename__ = "Pagos"
    ID_Pago = Column(Integer, primary_key=True, index=True)
    ID_Factura_Venta = Column(Integer, ForeignKey('Facturas_Venta.ID_Factura_Venta'), nullable=False, index=True)
    Metodo = Column(String(30), nullable=False, index=True)
    Monto = Column(Numeric(10, 2), nullable=False)
    Numero_Comprobante = Column(String(50), nullable=True)
    Fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    factura = relationship("Facturas_Venta", back_populates="pagos")
    usuario = relationship("Usuarios", back_populates="pagos")

    __table_args__ = (
        CheckConstraint('Monto > 0', name='CK_Pagos_Monto'),
        CheckConstraint("Metodo IN ('Efectivo', 'Tarjeta', 'Transferencia', 'Cheque')", 
                       name='CK_Pagos_Metodo'),
        Index('IX_Pagos_Factura', 'ID_Factura_Venta'),
        Index('IX_Pagos_Usuario', 'ID_Usuario'),
        Index('IX_Pagos_Fecha', 'Fecha'),
        Index('IX_Pagos_Metodo', 'Metodo')
    )

    def __repr__(self):
        return f"<Pago(ID_Pago={self.ID_Pago}, Metodo='{self.Metodo}', Monto={self.Monto})>"
    