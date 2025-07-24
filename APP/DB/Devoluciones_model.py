from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Devoluciones(Base):
    __tablename__ = "Devoluciones"
    ID_Devolucion = Column(Integer, primary_key=True, index=True)
    ID_Factura_Venta = Column(Integer, ForeignKey('Facturas_Venta.ID_Factura_Venta'), nullable=False, index=True)
    Fecha_Devolucion = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Motivo = Column(String(200), nullable=False)
    Estado = Column(String(30), nullable=False, default='Pendiente', index=True)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    factura = relationship("Facturas_Venta", back_populates="devoluciones")
    usuario = relationship("Usuarios", back_populates="devoluciones")
    detalles = relationship("Detalles_Devolucion", back_populates="devolucion", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("Estado IN ('Pendiente', 'Aprobada', 'Rechazada', 'Completada')", 
                       name='CK_Devoluciones_Estado'),
        Index('IX_Devoluciones_Factura', 'ID_Factura_Venta'),
        Index('IX_Devoluciones_Fecha', 'Fecha_Devolucion'),
        Index('IX_Devoluciones_Estado', 'Estado'),
        Index('IX_Devoluciones_Usuario', 'ID_Usuario')
    )

    def __repr__(self):
        return f"<Devolucion(ID_Devolucion={self.ID_Devolucion}, Estado='{self.Estado}')>"
    