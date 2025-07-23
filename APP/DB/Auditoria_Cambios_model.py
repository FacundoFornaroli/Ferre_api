from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from sqlalchemy.orm import relationship
from database import Base 
from datetime import datetime

class Auditoria_Cambios(Base):
    __tablename__ = "Auditoria_Cambios"
    ID_Auditoria = Column(Integer, primary_key=True, index=True)
    Tabla_Afectada = Column(String(100), nullable=False)
    ID_Registro = Column(Integer, nullable=False)
    Tipo_Operacion = Column(String(20), nullable=False)
    Fecha_Operacion = Column(DateTime, nullable=False, default=datetime.now)
    ID_Usuario = Column(Integer, ForeignKey('Usuarios.ID_Usuario'), nullable=False)
    Datos_Anteriores = Column(Text, nullable=True)
    Datos_Nuevos = Column(Text, nullable=True)
    IP_Cliente = Column(String(45), nullable=True)

    __table_args__ = (
        Index('IX_Auditoria_Tabla', 'Tabla_Afectada'),
        Index('IX_Auditoria_Fecha', 'Fecha_Operacion'),
        Index('IX_Auditoria_Usuario', 'ID_Usuario'),
    )

    def __repr__(self):
        return f"<Auditoria_Cambios(ID_Auditoria={self.ID_Auditoria}, Tabla_Afectada={self.Tabla_Afectada}, ID_Registro={self.ID_Registro}, Tipo_Operacion={self.Tipo_Operacion}, Fecha_Operacion={self.Fecha_Operacion}, ID_Usuario={self.ID_Usuario}, Datos_Anteriores={self.Datos_Anteriores}, Datos_Nuevos={self.Datos_Nuevos}, IP_Cliente={self.IP_Cliente})>"
    
    # Relaciones
    usuario = relationship("Usuarios", back_populates="auditoria_cambios")

        