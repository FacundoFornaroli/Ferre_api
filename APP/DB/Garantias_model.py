from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Garantias(Base):
    __tablename__ = "Garantias"
    ID_Garantia = Column(Integer, primary_key=True, index=True)
    ID_Producto = Column(Integer, ForeignKey('Productos.ID_Producto'), nullable=False, index=True)
    Tiempo_Garantia = Column(Integer, nullable=False)
    Tipo_Garantia = Column(String(50), nullable=False, index=True)
    Descripcion = Column(Text, nullable=True)
    Activo = Column(Boolean, nullable=False, default=True, index=True)

    # Relaciones
    producto = relationship("Productos", back_populates="garantias")

    __table_args__ = (
        CheckConstraint("Tipo_Garantia IN ('Fábrica', 'Local', 'Extendida')", 
                       name='CK_Garantias_Tipo'),
        CheckConstraint("Tiempo_Garantia > 0", 
                       name='CK_Garantias_Tiempo'),
        Index('IX_Garantias_Producto', 'ID_Producto'),
        Index('IX_Garantias_Tipo', 'Tipo_Garantia'),
        Index('IX_Garantias_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Garantia(ID_Garantia={self.ID_Garantia}, Tipo_Garantia='{self.Tipo_Garantia}', Tiempo_Garantia={self.Tiempo_Garantia})>"
    