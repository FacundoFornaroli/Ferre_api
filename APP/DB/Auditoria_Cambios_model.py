from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Auditoria_Cambios(Base):
    __tablename__ = "Auditoria_Cambios"
    ID_Auditoria = Column(Integer, primary_key=True, index=True)
    Tabla_Afectada = Column(String(100), nullable=False, index=True)
    ID_Registro = Column(Integer, nullable=False)
    Tipo_Operacion = Column(String(20), nullable=False, index=True)
    Fecha_Operacion = Column(DateTime, nullable=False, default=datetime.now, index=True)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False, index=True)
    Datos_Anteriores = Column(Text, nullable=True)
    Datos_Nuevos = Column(Text, nullable=True)
    IP_Cliente = Column(String(45), nullable=True)

    # Relaciones
    usuario = relationship("Usuarios", back_populates="auditoria_cambios")

    __table_args__ = (
        CheckConstraint("Tipo_Operacion IN ('INSERT', 'UPDATE', 'DELETE')", 
                       name='CK_Auditoria_TipoOperacion'),
        Index('IX_Auditoria_Tabla', 'Tabla_Afectada'),
        Index('IX_Auditoria_Fecha', 'Fecha_Operacion'),
        Index('IX_Auditoria_Usuario', 'ID_Usuario'),
        Index('IX_Auditoria_TipoOperacion', 'Tipo_Operacion'),
        Index('IX_Auditoria_Registro', 'ID_Registro')
    )

    def __repr__(self):
        return f"<AuditoriaCambio(ID_Auditoria={self.ID_Auditoria}, Tabla='{self.Tabla_Afectada}', Operacion='{self.Tipo_Operacion}')>"