from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Garantias(Base):
    __tablename__ = "Garantias"
    ID_Garantia = Column(Integer, primary_key=True, index=Ture)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Tiempo_Garantia = Column(Integer, nullable=False)
    Tipo_Garantia = Column(String(50), nullable=False)
    Descripcion = Column(Text, nullable=True)
    Activo = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        CheckConstraint("Tipo_Garantia IN ('Fábrica', 'Local', 'Extendida')", name='CK_Garantias_Tipo'),
        Index('IX_Garantias_Producto', 'ID_Producto'),
        Index('IX_Garantias_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Garantias(ID_Garantia={self.ID_Garantia}, ID_Producto={self.ID_Producto}, Tiempo_Garantia={self.Tiempo_Garantia}, Tipo_Garantia={self.Tipo_Garantia}, Descripcion={self.Descripcion}, Activo={self.Activo})>"
    