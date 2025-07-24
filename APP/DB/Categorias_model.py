from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Categorias(Base):
    __tablename__ = "Categorias"
    
    ID_Categoria = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False, unique=True)
    Descripcion = Column(String(500), nullable=True)
    Categoria_Padre = Column(Integer, ForeignKey('Categorias.ID_Categoria'), nullable=True, index=True)
    Activo = Column(Boolean, default=True, nullable=False, index=True)
    Fecha_Creacion = Column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    subcategorias = relationship("Categorias", backref="padre", remote_side=[ID_Categoria])
    productos = relationship("Productos", back_populates="categoria")

    __table_args__ = (
        Index('IX_Categorias_Padre', 'Categoria_Padre'),
        Index('IX_Categorias_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Categoria(ID_Categoria={self.ID_Categoria}, Nombre='{self.Nombre}', Activo={self.Activo})>"

