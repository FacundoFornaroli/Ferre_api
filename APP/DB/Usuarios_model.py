from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Usuarios(Base):
    __tablename__ = "Usuarios"
    
    ID_Usuario = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Apellido = Column(String(100), nullable=False)
    CUIL = Column(String(13), unique=True)
    Rol = Column(String(50), nullable=False)
    Email = Column(String(120), unique=True, nullable=False)
    Contraseña = Column(String(255), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'))
    Estado = Column(Boolean, default=True, nullable=False)
    Ultimo_Acceso = Column(DateTime, nullable=True)
    Creado_el = Column(DateTime, default=datetime.now, nullable=False)
    Actualizado_el = Column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    sucursal = relationship("Sucursales", back_populates="usuarios")
    facturas_venta = relationship("Facturas_Venta", back_populates="usuario")
    pagos = relationship("Pagos", back_populates="usuario")
    ordenes_compra = relationship("Ordenes_Compra", back_populates="usuario")
    movimientos_inventario = relationship("Movimientos_inventario", back_populates="usuario")
    devoluciones = relationship("Devoluciones", back_populates="usuario")
    transferencias_solicitadas = relationship(
        "Transferencias_Sucursales",
        foreign_keys="Transferencias_Sucursales.ID_Usuario_Solicitante",
        back_populates="usuario_solicitante"
    )
    transferencias_autorizadas = relationship(
        "Transferencias_Sucursales",
        foreign_keys="Transferencias_Sucursales.ID_Usuario_Autorizador",
        back_populates="usuario_autorizador"
    )
    auditoria_cambios = relationship("Auditoria_Cambios", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario(ID_Usuario={self.ID_Usuario}, Email='{self.Email}', Rol='{self.Rol}')>"
        