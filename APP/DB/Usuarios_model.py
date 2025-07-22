from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, true
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuarios(Base):
    __tablename__ = "Usuarios"
    ID_Usuario = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Apellido = Column(String(100), nullable=False)
    CUIL = Column(String(13), nullable=True, unique=True)
    Rol = Column(String(50), nullable=False)
    Email = Column(String(120), nullable=False, unique=True)
    Contraseña = Column(String(255), nullable=False)
    ID_Sucursal = Column(Integer, ForeignKey('Sucursales.ID_Sucursal'), nullable=True)
    Estado = Column(Boolean, default=True, nullable=False)
    Ultimo_Acceso = Column(DateTime, nullable=True)
    Creado_el = Column(DateTime, default=datetime.now, nullable=False)
    Actualizado_el = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Usuario(ID_Usuario={self.ID_Usuario}, Nombre='{self.Nombre}', Apellido='{self.Apellido}', Email='{self.Email}', Rol='{self.Rol}', Estado={self.Estado})>"
        