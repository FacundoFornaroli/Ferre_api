from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Movimientos_inventario(Base):
    __tablename__ = "Movimientos_inventario"
    ID_Movimiento = Column(Integer, primary_key=True, index=False)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False)
    Fecha = Column(DateTime, nullable=False)
    Tipo = Column(String(15), nullable=False)
    Cantidad = Column(Integer, nullable=False)
    Costo_Unitario = Column(Numeric(10, 2), nullable=True)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    ID_Referencia = Column(Integer, nullable=True)
    Tipo_Referencia = Column(String(20), nullable=True)
    Observaciones = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint('Tipo IN ("Compra", "Venta", "Transferencia", "Ajuste", "Devolucion")', name='CK_MovimientosInventario_Tipo'),
    )

    def __repr__(self):
        return f"<Movimientos_inventario(ID_Movimiento={self.ID_Movimiento}, ID_Producto={self.ID_Producto}, ID_Sucursal={self.ID_Sucursal}, Fecha={self.Fecha}, Tipo={self.Tipo}, Cantidad={self.Cantidad}, Costo_Unitario={self.Costo_Unitario}, ID_Usuario={self.ID_Usuario}, ID_Referencia={self.ID_Referencia}, Tipo_Referencia={self.Tipo_Referencia}, Observaciones={self.Observaciones})>"