from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Index, UniqueConstraint, and_
from sqlalchemy.orm import relationship, foreign, remote
from database import Base
from datetime import datetime

class Inventario(Base):
    __tablename__ = "Inventario"
    
    ID_Inventario = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False)
    Stock_Actual = Column(Integer, nullable=False, default=0)
    Stock_Minimo = Column(Integer, nullable=False, default=0)
    Stock_Maximo = Column(Integer, nullable=False, default=0)
    Ubicacion = Column(String(100))
    Fecha_Ultimo_Movimiento = Column(DateTime)
    Activo = Column(Boolean, nullable=False, default=True)

    # Relaciones
    producto = relationship("Productos", back_populates="inventarios")
    sucursal = relationship("Sucursales", back_populates="inventario")
    movimientos = relationship(
        "Movimientos_inventario",
        primaryjoin="and_(foreign(Inventario.ID_Producto)==remote(Movimientos_inventario.ID_Producto), "
                   "foreign(Inventario.ID_Sucursal)==remote(Movimientos_inventario.ID_Sucursal))",
        back_populates="inventario",
        viewonly=True
    )

    __table_args__ = (
        CheckConstraint('Stock_Minimo >= 0', name='CK_Inventario_Stock_Minimo'),
        CheckConstraint('Stock_Maximo >= Stock_Minimo', name='CK_Inventario_Stock_Maximo'),
        UniqueConstraint('ID_Producto', 'ID_Sucursal', name='UQ_Inventario_Producto_Sucursal'),
        Index('IX_Inventario_Producto', 'ID_Producto'),
        Index('IX_Inventario_Sucursal', 'ID_Sucursal'),
        Index('IX_Inventario_Stock', 'Stock_Actual', 'Stock_Minimo')
    )

    def __repr__(self):
        return f"<Inventario(ID_Inventario={self.ID_Inventario}, ID_Producto={self.ID_Producto}, Stock_Actual={self.Stock_Actual})>"
        