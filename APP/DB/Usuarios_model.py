from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, true
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuarios(Base):
    __tablename__ = "Usuarios"
    ID_Usuario = Column(Integer, primary_key=True, index=True)
    