from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Movimientos_inventario(Base):
    __tablename__ = "Movimientos_inventario"
    
    ID_Movimiento = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    Fecha = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Tipo = Column(String(15), nullable=False, index=True)
    Cantidad = Column(Integer, nullable=False)
    Costo_Unitario = Column(Numeric(10, 2), nullable=True)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    ID_Referencia = Column(Integer, nullable=True)
    Tipo_Referencia = Column(String(20), nullable=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    producto = relationship("Productos", back_populates="movimientos_inventario")
    sucursal = relationship("Sucursales", back_populates="movimientos_inventario")
    usuario = relationship("Usuarios", back_populates="movimientos_inventario")

    __table_args__ = (
        CheckConstraint("Tipo IN ('Compra', 'Venta', 'Transferencia', 'Ajuste', 'Devolucion')", 
                       name='CK_MovimientosInventario_Tipo'),
        Index('IX_MovimientosInventario_Producto', 'ID_Producto'),
        Index('IX_MovimientosInventario_Sucursal', 'ID_Sucursal'),
        Index('IX_MovimientosInventario_Fecha', 'Fecha'),
        Index('IX_MovimientosInventario_Usuario', 'ID_Usuario'),
        Index('IX_MovimientosInventario_Tipo', 'Tipo')
    )

    def __repr__(self):
        return f"<Movimientos_inventario(ID_Movimiento={self.ID_Movimiento}, ID_Producto={self.ID_Producto}, ID_Sucursal={self.ID_Sucursal}, Fecha={self.Fecha}, Tipo={self.Tipo}, Cantidad={self.Cantidad}, Costo_Unitario={self.Costo_Unitario}, ID_Usuario={self.ID_Usuario}, ID_Referencia={self.ID_Referencia}, Tipo_Referencia={self.Tipo_Referencia}, Observaciones={self.Observaciones})>"
        