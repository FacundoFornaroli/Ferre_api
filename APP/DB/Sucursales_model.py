from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, ForeignKey, CheckConstraint, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Sucursales(Base):
    __tablename__ = "Sucursales"
    
    ID_Sucursal = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False, unique=True)
    Direccion = Column(String(200), nullable=False)
    Telefono = Column(String(40))
    Email = Column(String(120))
    Localidad = Column(String(100), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Codigo_Postal = Column(String(10))
    Horario_Apertura = Column(Time)
    Horario_Cierre = Column(Time)
    Activo = Column(Boolean, default=True, nullable=False)
    Fecha_Creacion = Column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    usuarios = relationship("Usuarios", back_populates="sucursal")
    inventario = relationship("Inventario", back_populates="sucursal")
    facturas_venta = relationship("Facturas_Venta", back_populates="sucursal")
    ordenes_compra = relationship("Ordenes_Compra", back_populates="sucursal")
    movimientos = relationship("Movimientos_inventario", back_populates="sucursal")
    transferencias_origen = relationship(
        "Transferencias_Sucursales",
        foreign_keys="Transferencias_Sucursales.ID_Sucursal_Origen",
        back_populates="sucursal_origen"
    )
    transferencias_destino = relationship(
        "Transferencias_Sucursales",
        foreign_keys="Transferencias_Sucursales.ID_Sucursal_Destino",
        back_populates="sucursal_destino"
    )

    __table_args__ = (
        CheckConstraint('Horario_Cierre > Horario_Apertura', name='CK_Sucursales_Horario'),
        Index('IX_Sucursales_Provincia', 'Provincia'),
        Index('IX_Sucursales_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Sucursal(ID_Sucursal={self.ID_Sucursal}, Nombre='{self.Nombre}', Activo={self.Activo})>"
