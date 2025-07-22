from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Facturas_Venta(Base):
    __tablename__ = "Facturas_Venta"
    ID_Factura_Venta = Column(Integer, primary_key=True, index=True)
    Numero_Factura = Column(String(20), nullable=True, unique=True)
    ID_Cliente = Column(Integer, ForeignKey('Clientes.ID_Cliente'), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False)
    Fecha = Column(DateTime, nullable=False, default=datetime.now)
    Tipo_Factura = Column(String(1), nullable=False, default='B')
    Condicion_IVA = Column(String(50), nullable=True)
    Subtotal = Column(Numeric(10, 2), nullable=False)
    IVA = Column(Numeric(10, 2), nullable=False, default=0)
    Descuento = Column(Numeric(10, 2), nullable=False, default=0)
    Total = Column(Numeric(10, 2), nullable=False)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    Estado = Column(String(30), nullable=False, default='Emitida')
    Forma_Pago = Column(String(50), nullable=True)
    Observaciones = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Factura_Venta(ID_Factura_Venta={self.ID_Factura_Venta}, Numero_Factura='{self.Numero_Factura}', ID_Cliente={self.ID_Cliente}, ID_Sucursal={self.ID_Sucursal}, Fecha='{self.Fecha}', Tipo_Factura='{self.Tipo_Factura}', Condicion_IVA='{self.Condicion_IVA}', Subtotal={self.Subtotal}, IVA={self.IVA}, Descuento={self.Descuento}, Total={self.Total}, ID_Usuario={self.ID_Usuario}, Estado='{self.Estado}', Forma_Pago='{self.Forma_Pago}', Observaciones='{self.Observaciones}')>"
        