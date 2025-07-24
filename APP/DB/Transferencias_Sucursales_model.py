from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Transferencias_Sucursales(Base):
    __tablename__ = "Transferencias_Sucursales"
    ID_Transferencia = Column(Integer, primary_key=True, index=True)
    Numero_Transferencia = Column(String(20), nullable=True, unique=True)
    ID_Sucursal_Origen = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    ID_Sucursal_Destino = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=False, index=True)
    Fecha_Solicitud = Column(DateTime, nullable=False, default=datetime.now, index=True)
    Fecha_Transferencia = Column(DateTime, nullable=True, index=True)
    Estado = Column(String(30), nullable=False, default='Pendiente', index=True)
    ID_Usuario_Solicitante = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    ID_Usuario_Autorizador = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=True, index=True)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    sucursal_origen = relationship("Sucursales", foreign_keys=[ID_Sucursal_Origen], back_populates="transferencias_origen")
    sucursal_destino = relationship("Sucursales", foreign_keys=[ID_Sucursal_Destino], back_populates="transferencias_destino")
    usuario_solicitante = relationship("Usuarios", foreign_keys=[ID_Usuario_Solicitante], back_populates="transferencias_solicitadas")
    usuario_autorizador = relationship("Usuarios", foreign_keys=[ID_Usuario_Autorizador], back_populates="transferencias_autorizadas")
    detalles = relationship("Detalles_Transferencia", back_populates="transferencia", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("ID_Sucursal_Origen != ID_Sucursal_Destino", name='CK_Transferencias_Sucursales'),
        CheckConstraint("Estado IN ('Pendiente', 'Aprobada', 'En Tránsito', 'Completada', 'Cancelada')", 
                       name='CK_Transferencias_Estado'),
        Index('IX_Transferencias_Origen', 'ID_Sucursal_Origen'),
        Index('IX_Transferencias_Destino', 'ID_Sucursal_Destino'),
        Index('IX_Transferencias_FechaSolicitud', 'Fecha_Solicitud'),
        Index('IX_Transferencias_Estado', 'Estado'),
        Index('IX_Transferencias_UsuarioSolicitante', 'ID_Usuario_Solicitante'),
        Index('IX_Transferencias_UsuarioAutorizador', 'ID_Usuario_Autorizador')
    )

    def __repr__(self):
        return f"<Transferencia(ID_Transferencia={self.ID_Transferencia}, Estado='{self.Estado}')>"
    
    