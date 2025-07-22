from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Ordenes_Compra(Base):
    __tablename__ = "Ordenes_Compra"
    ID_OC = Column(Integer, primary_key=True, index=True)
    Numero_OC = Column(String(20), nullable=True, unique=True)
    ID_Proveedor = Column(Integer, ForeignKey('Proveedores.ID_Proveedor'), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False)
    Fecha = Column(DateTime, nullable=False, default=datetime.now)
    Fecha_Entrega_Esperada = Column(Date, nullable=True)
    Subtotal = Column(Numeric(10, 2), nullable=False)
    IVA = Column(Numeric(10, 2), nullable=False, default=0)
    Descuento = Column(Numeric(10, 2), nullable=False, default=0)
    Total = Column(Numeric(10, 2), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    Estado = Column(String(30), nullable=False, default='Pendiente')  # 'Pendiente', 'Aprobada', 'Recibida', 'Cancelada'
    Observaciones = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint('Total > 0', name='CK_OrdenesCompra_Total')
    )

    def __repr__(self):
        return f"<OrdenCompra(ID_OC={self.ID_OC}, Numero_OC='{self.Numero_OC}', ID_Proveedor={self.ID_Proveedor}, ID_Sucursal={self.ID_Sucursal}, Fecha='{self.Fecha}', Fecha_Entrega_Esperada='{self.Fecha_Entrega_Esperada}', Subtotal={self.Subtotal}, IVA={self.IVA}, Descuento={self.Descuento}, Total={self.Total}, ID_Usuario={self.ID_Usuario}, Estado='{self.Estado}')>"
        