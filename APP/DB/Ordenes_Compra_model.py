from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Date, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Ordenes_Compra(Base):
    __tablename__ = "Ordenes_Compra"
    ID_OC = Column(Integer, primary_key=True, index=True)
    Numero_OC = Column(String(20), nullable=True, unique=True)
    ID_Proveedor = Column(Integer, ForeignKey('Proveedores.ID_Proveedor'), nullable=False, index=True)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    Fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Fecha_Entrega_Esperada = Column(Date, nullable=True)
    Subtotal = Column(Numeric(10, 2), nullable=False)
    IVA = Column(Numeric(10, 2), nullable=False, default=0)
    Descuento = Column(Numeric(10, 2), nullable=False, default=0)
    Total = Column(Numeric(10, 2), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Estado = Column(String(30), nullable=False, default='Pendiente', index=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    proveedor = relationship("Proveedores", back_populates="ordenes_compra")
    sucursal = relationship("Sucursales", back_populates="ordenes_compra")
    usuario = relationship("Usuarios", back_populates="ordenes_compra")
    detalles = relationship("Detalle_OC", back_populates="orden", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('Total > 0', name='CK_OrdenesCompra_Total'),
        CheckConstraint("Estado IN ('Pendiente', 'Aprobada', 'Recibida', 'Cancelada')", 
                       name='CK_OrdenesCompra_Estado'),
        Index('IX_OrdenesCompra_Proveedor', 'ID_Proveedor'),
        Index('IX_OrdenesCompra_Sucursal', 'ID_Sucursal'),
        Index('IX_OrdenesCompra_Usuario', 'ID_Usuario'),
        Index('IX_OrdenesCompra_Fecha', 'Fecha'),
        Index('IX_OrdenesCompra_Estado', 'Estado')
    )

    def __repr__(self):
        return f"<OrdenCompra(ID_OC={self.ID_OC}, Numero_OC='{self.Numero_OC}', Estado='{self.Estado}')>"
        