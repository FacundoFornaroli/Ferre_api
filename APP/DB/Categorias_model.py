from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime, Boolean, DateTime



class Categorias(Base):
    __tablename__ = "Categorias"
    ID_Categoria = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Descripcion = Column(String(500), nullable=True)
    Categoria_Padre = Column(Integer, nullable=True)
    Activo = Column(Boolean, default=True)
    Fecha_Creacion = Column(Datetime, default=datetime.now)


