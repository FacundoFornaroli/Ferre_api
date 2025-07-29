from sqlalchemy import Column, Integer, String, Boolean, Index
from database import Base 
from sqlalchemy.orm import relationship

class Unidades_de_medida(Base):
    __tablename__ = "Unidades_de_medida"
    ID_Unidad_de_medida = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(50), nullable=False, unique=True)
    Abreviatura = Column(String(10), nullable=False)
    Activo = Column(Boolean, nullable=False, default=True, index=True)

    # Relaciones
    productos = relationship("Productos", back_populates="unidad_medida")

    __table_args__ = (
        Index('IX_Unidades_de_medida_Nombre', 'Nombre'),
        Index('IX_Unidades_de_medida_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Unidad_de_medida(ID_Unidad_de_medida={self.ID_Unidad_de_medida}, Nombre='{self.Nombre}', Abreviatura='{self.Abreviatura}')>"
