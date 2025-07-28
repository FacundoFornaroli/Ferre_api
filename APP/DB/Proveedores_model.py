from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Proveedores(Base):
    __tablename__ = "Proveedores"
    ID_Proveedor = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(150), nullable=False)
    CUIT = Column(String(13), nullable=True, unique=True)
    Condicion_IVA = Column(String(50), nullable=True)
    Direccion = Column(String(200), nullable=False)
    Localidad = Column(String(100), nullable=False)
    Provincia = Column(String(50), nullable=False)
    Codigo_Postal = Column(String(10), nullable=True)
    Telefono = Column(String(40), nullable=False)
    Telefono_Alternativo = Column(String(40), nullable=True)
    Email = Column(String(120), nullable=True)
    Contacto_Persona = Column(String(100), nullable=True)
    Plazo_Entrega = Column(Integer, nullable=True)
    Activo = Column(Boolean, default=True, nullable=False)
    Fecha_Creacion = Column(DateTime, default=datetime.now, nullable=False)
    Observaciones = Column(Text, nullable=True)

    # Relaciones
    ordenes_compra = relationship("Ordenes_Compra", back_populates="proveedor")

    def __repr__(self):
        return f"<Proveedor(ID_Proveedor={self.ID_Proveedor}, Nombre='{self.Nombre}', CUIT='{self.CUIT}', Condicion_IVA='{self.Condicion_IVA}', Direccion='{self.Direccion}', Localidad='{self.Localidad}', Provincia='{self.Provincia}', Codigo_Postal='{self.Codigo_Postal}', Telefono='{self.Telefono}', Telefono_Alternativo='{self.Telefono_Alternativo}', Email='{self.Email}', Contacto_Persona='{self.Contacto_Persona}', Plazo_Entrega='{self.Plazo_Entrega}', Activo='{self.Activo}', Fecha_Creacion='{self.Fecha_Creacion}', Observaciones='{self.Observaciones}')>"
        
