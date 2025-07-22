from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from datetime import datetime

class Pagos(Base):
    __tablename__ = "Pagos"
    ID_Pago = Column(Integer, primary_key=True, index=True)
    ID_Factura_Venta = Column(Integer, ForeignKey('Facturas_Venta.ID_Factura_Venta'), nullable=False)
    Metodo = Column(String(30), nullable=False)  # 'Efectivo', 'Tarjeta', 'Transferencia', 'Cheque'
    Monto = Column(Numeric(10, 2), nullable=False)
    Numero_Comprobante = Column(String(50), nullable=True)
    Fecha = Column(DateTime, nullable=False, default=datetime.now)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    Observaciones = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint('Monto > 0', name='CK_Pagos_Monto'),
    )

    def __repr__(self):
        return f"<Pago(ID_Pago={self.ID_Pago}, Metodo='{self.Metodo}', Monto={self.Monto})>"
    