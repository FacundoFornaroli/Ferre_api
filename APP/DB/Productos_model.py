from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index, UniqueConstraint
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
    ID_Categoria = Column(Integer, ForeignKey('Categorias.ID_Categoria'), nullable=False, index=True)
    ID_Unidad_de_medida = Column(Integer, ForeignKey('Unidades_de_medida.ID_Unidad_de_medida'), nullable=False, index=True)
    Peso = Column(Numeric(8, 2), nullable=True)
    Dimensiones = Column(String(50), nullable=True)
    Activo = Column(Boolean, default=True, nullable=False, index=True)
    Fecha_Creacion = Column(DateTime, default=datetime.now, nullable=False)
    Fecha_Actualizacion = Column(DateTime, default=datetime.now, nullable=False)

    # Relaciones
    categoria = relationship("Categorias", back_populates="productos")
    unidad_medida = relationship("Unidades_de_medida", back_populates="productos")
    inventarios = relationship("Inventario", back_populates="producto")
    detalles_factura = relationship("Detalles_Factura_Venta", back_populates="producto")
    detalles_oc = relationship("Detalle_OC", back_populates="producto")
    movimientos_inventario = relationship("Movimientos_inventario", back_populates="producto")
    garantias = relationship("Garantias", back_populates="producto")
    productos_descuentos = relationship("Productos_Descuentos", back_populates="producto")
    descuentos = relationship("Descuentos", secondary="Productos_Descuentos", back_populates="productos")
    detalles_devolucion = relationship("Detalles_Devolucion", back_populates="producto")
    detalles_transferencia = relationship("Detalles_Transferencia", back_populates="producto")

    __table_args__ = (
        CheckConstraint('Precio > 0', name='CK_Productos_Precio'),
        CheckConstraint('Costo > 0', name='CK_Productos_Costo'),
        Index('IX_Productos_Categoria', 'ID_Categoria'),
        Index('IX_Productos_Unidad', 'ID_Unidad_de_medida'),
        Index('IX_Productos_CodigoBarras', 'Codigo_Barras'),
        Index('IX_Productos_SKU', 'SKU'),
        Index('IX_Productos_Marca', 'Marca'),
        Index('IX_Productos_Activo', 'Activo')
    )

    def __repr__(self):
        return f"<Producto(ID_Producto={self.ID_Producto}, Nombre='{self.Nombre}', Activo={self.Activo})>"

