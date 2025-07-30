from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index, and_
from sqlalchemy.orm import relationship, foreign, remote
from database import Base
from datetime import datetime

class Movimientos_inventario(Base):
    __tablename__ = "Movimientos_inventario"
    
    ID_Movimiento = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False)
    ID_Inventario = Column(Integer, ForeignKey('Inventario.ID_Inventario'), nullable=False)
    Fecha = Column(DateTime, nullable=False, default=datetime.now)
    Tipo = Column(String(15), nullable=False)  # 'Compra', 'Venta', 'Transferencia', 'Ajuste', 'Devolucion'
    Cantidad = Column(Integer, nullable=False)
    Costo_Unitario = Column(Numeric(10, 2))
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    ID_Referencia = Column(Integer)  # ID de la factura, OC, transferencia, etc.
    Tipo_Referencia = Column(String(20))  # 'Factura', 'OC', 'Transferencia', etc.
    Observaciones = Column(Text)

    # Relaciones
    producto = relationship("Productos", back_populates="movimientos_inventario")
    sucursal = relationship("Sucursales", back_populates="movimientos_inventario")
    usuario = relationship("Usuarios", back_populates="movimientos_inventario")
    inventario = relationship("Inventario", back_populates="movimientos")

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
        return f"<Movimiento_inventario(ID_Movimiento={self.ID_Movimiento}, Tipo='{self.Tipo}', Cantidad={self.Cantidad})>"
        