from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Productos(Base):
    __tablename__ = "Productos"
    ID_Producto = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(150), nullable=False)
    Descripcion = Column(Text, nullable=True)
    Codigo_Barras = Column(String(50), nullable=True, unique=True)
    SKU = Column(String(20), nullable=True, unique=True)
    Marca = Column(String(100), nullable=True)
    Modelo = Column(String(100), nullable=True)
    Precio = Column(Numeric(10, 2), nullable=False)
    Costo = Column(Numeric(10, 2), nullable=False)
    Precio_Mayorista = Column(Numeric(10, 2), nullable=True)
    ID_Categoria = Column(Integer, ForeignKey('Categorias.ID_Categoria'), nullable=False)
    ID_Unidad_de_medida = Column(Integer, ForeignKey('Unidades_de_medida.ID_Unidad_de_medida'), nullable=False)
    Peso = Column(Numeric(8, 2), nullable=True)
    Dimensiones = Column(String(50), nullable=True)
    Activo = Column(Boolean, default=True, nullable=False)
    Fecha_Creacion = Column(DateTime, default=datetime.now, nullable=False)
    Fecha_Actualizacion = Column(DateTime, default=datetime.now, nullable=False)

    def __repr__(self):
        return f"<Producto(ID_Producto={self.ID_Producto}, Nombre='{self.Nombre}', Activo={self.Activo})>"

