from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index, UniqueConstraint
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Inventario(Base):
    __tablename__ = "Inventario"
    ID_Inventario = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    Stock_Actual = Column(Integer, nullable=False, default=0)
    Stock_Minimo = Column(Integer, nullable=False, default=0)
    Stock_Maximo = Column(Integer, nullable=False, default=0)
    Ubicacion = Column(String(100), nullable=True)
    Fecha_Ultimo_Movimiento = Column(DateTime, nullable=True)
    Activo = Column(Boolean, default=True, nullable=False)

    # Relaciones
    producto = relationship("Productos", back_populates="inventarios")
    sucursal = relationship("Sucursales", back_populates="inventarios")

    __table_args__ = (
        CheckConstraint('Stock_Minimo >= 0', name='CK_Inventario_Stock_Minimo'),
        CheckConstraint('Stock_Maximo >= Stock_Minimo', name='CK_Inventario_Stock_Maximo'),
        UniqueConstraint('ID_Producto', 'ID_Sucursal', name='UQ_Inventario_Producto_Sucursal'),
        Index('IX_Inventario_Producto', 'ID_Producto'),
        Index('IX_Inventario_Sucursal', 'ID_Sucursal'),
        Index('IX_Inventario_Stock', 'Stock_Actual', 'Stock_Minimo')
    )

    def __repr__(self):
        return f"<Inventario(ID_Inventario={self.ID_Inventario}, ID_Producto={self.ID_Producto}, ID_Sucursal={self.ID_Sucursal}, Stock_Actual={self.Stock_Actual}, Stock_Minimo={self.Stock_Minimo}, Stock_Maximo={self.Stock_Maximo}, Ubicacion='{self.Ubicacion}', Fecha_Ultimo_Movimiento='{self.Fecha_Ultimo_Movimiento}', Activo={self.Activo})>"
        