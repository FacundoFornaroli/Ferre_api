from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Facturas_Venta(Base):
    __tablename__ = "Facturas_Venta"
    ID_Factura_Venta = Column(Integer, primary_key=True, index=True)
    Numero_Factura = Column(String(20), nullable=True, unique=True)
    ID_Cliente = Column(Integer, ForeignKey('Clientes.ID_Cliente'), nullable=False, index=True)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    Fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Tipo_Factura = Column(String(1), nullable=False, default='B', index=True)
    Condicion_IVA = Column(String(50), nullable=True)
    Subtotal = Column(Numeric(10, 2), nullable=False)
    IVA = Column(Numeric(10, 2), nullable=False, default=0)
    Descuento = Column(Numeric(10, 2), nullable=False, default=0)
    Total = Column(Numeric(10, 2), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Estado = Column(String(30), nullable=False, default='Emitida', index=True)
    Forma_Pago = Column(String(50), nullable=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    cliente = relationship("Clientes", back_populates="facturas")
    sucursal = relationship("Sucursales", back_populates="facturas_venta")
    usuario = relationship("Usuarios", back_populates="facturas")
    detalles = relationship("Detalles_Factura_Venta", back_populates="factura", cascade="all, delete-orphan")
    pagos = relationship("Pagos", back_populates="factura")
    devoluciones = relationship("Devoluciones", back_populates="factura")

    __table_args__ = (
        CheckConstraint("Tipo_Factura IN ('A', 'B', 'C')", name='CK_FacturasVenta_Tipo'),
        CheckConstraint('Total > 0', name='CK_FacturasVenta_Total'),
        Index('IX_FacturasVenta_Cliente', 'ID_Cliente'),
        Index('IX_FacturasVenta_Sucursal', 'ID_Sucursal'),
        Index('IX_FacturasVenta_Usuario', 'ID_Usuario'),
        Index('IX_FacturasVenta_Fecha', 'Fecha'),
        Index('IX_FacturasVenta_Tipo', 'Tipo_Factura'),
        Index('IX_FacturasVenta_Estado', 'Estado')
    )

    def __repr__(self):
        return f"<Factura_Venta(ID_Factura_Venta={self.ID_Factura_Venta}, Numero_Factura='{self.Numero_Factura}', Estado='{self.Estado}')>"
        