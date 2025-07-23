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
    Estado = Column(String(30), nullable=False, default='Pendiente')
    ID_Usuario_Solicitante = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    ID_Usuario_Autorizador = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=True, index=True)
    Observaciones = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("ID_Sucursal_Origen != ID_Sucursal_Destino", name='CK_Transferencias_Sucursales'),
        Index('IX_Transferencias_Origen', 'ID_Sucursal_Origen'),
        Index('IX_Transferencias_Destino', 'ID_Sucursal_Destino'),
        Index('IX_Transferencias_FechaSolicitud', 'Fecha_Solicitud'),
        Index('IX_Transferencias_Estado', 'Estado'),
    )

    def __repr__(self):
        return f"<Transferencias_Sucursales(ID_Transferencia={self.ID_Transferencia}, Numero_Transferencia={self.Numero_Transferencia}, ID_Sucursal_Origen={self.ID_Sucursal_Origen}, ID_Sucursal_Destino={self.ID_Sucursal_Destino}, Fecha_Solicitud={self.Fecha_Solicitud}, Fecha_Transferencia={self.Fecha_Transferencia}, Estado={self.Estado}, ID_Usuario_Solicitante={self.ID_Usuario_Solicitante}, ID_Usuario_Autorizador={self.ID_Usuario_Autorizador}, Observaciones={self.Observaciones})>"
    
    # Relaciones
    sucursal_origen = relationship("Sucursales", foreign_keys=[ID_Sucursal_Origen])
    sucursal_destino = relationship("Sucursales", foreign_keys=[ID_Sucursal_Destino])
    usuario_solicitante = relationship("Usuarios", foreign_keys=[ID_Usuario_Solicitante])
    usuario_autorizador = relationship("Usuarios", foreign_keys=[ID_Usuario_Autorizador])
    detalles_transferencia = relationship("Detalles_Transferencia", back_populates="transferencia")

    