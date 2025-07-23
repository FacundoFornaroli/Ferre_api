from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric
from database import Base 
from datetime import datetime

class Devoluciones(Base):
    __tablename__ = "Devoluciones"
    ID_Devolucion = Column(Integer, primary_key=True, index=True)
    ID_Factura_Venta = Column(Integer, ForeignKey('Facturas_Venta.ID_Factura_Venta'), nullable=False, index=True)
    Fecha_Devolucion = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Motivo = Column(String(200), nullable=False)
    Estado = Column(String(30), nullable=False, default='Pendiente')
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Observaciones = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("Estado IN ('Pendiente', 'Aprobada', 'Rechazada', 'Completada')", name='CK_Devoluciones_Estado'),
        Index('IX_Devoluciones_Factura', 'ID_Factura_Venta'),
        Index('IX_Devoluciones_Fecha', 'Fecha_Devolucion'),
        Index('IX_Devoluciones_Estado', 'Estado'),
    )

    def __repr__(self):
        return f"<Devoluciones(ID_Devolucion={self.ID_Devolucion}, ID_Factura_Venta={self.ID_Factura_Venta}, Fecha_Devolucion={self.Fecha_Devolucion}, Motivo={self.Motivo}, Estado={self.Estado}, ID_Usuario={self.ID_Usuario}, Observaciones={self.Observaciones})>"