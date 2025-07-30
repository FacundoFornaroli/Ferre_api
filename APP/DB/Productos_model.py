from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, CheckConstraint, Numeric, Text, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Productos(Base):
    __tablename__ = "Productos"
    
    ID_Producto = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(150), nullable=False)
    Descripcion = Column(Text)
    Codigo_Barras = Column(String(50), unique=True)
    SKU = Column(String(20), unique=True)
    Marca = Column(String(100))
    Modelo = Column(String(100))
    Precio = Column(Numeric(10, 2), nullable=False)
    Costo = Column(Numeric(10, 2), nullable=False)
    Precio_Mayorista = Column(Numeric(10, 2))
    ID_Categoria = Column(Integer, ForeignKey('Categorias.ID_Categoria'), nullable=False)
    ID_Unidad_de_medida = Column(Integer, ForeignKey('Unidades_de_medida.ID_Unidad_de_medida'), nullable=False)
    Peso = Column(Numeric(8, 2))  # en kg
    Dimensiones = Column(String(50))  # formato: LxAxH
    Activo = Column(Boolean, nullable=False, default=True)
    Fecha_Creacion = Column(DateTime, nullable=False, default=datetime.now)
    Fecha_Actualizacion = Column(DateTime, nullable=False, default=datetime.now)

    # Relaciones
    categoria = relationship("Categorias", back_populates="productos")
    unidad_medida = relationship("Unidades_de_medida", back_populates="productos")
    inventarios = relationship("Inventario", back_populates="producto")
    detalles_factura = relationship("Detalles_Factura_Venta", back_populates="producto")
    detalles_oc = relationship("Detalle_OC", back_populates="producto")
    movimientos = relationship("Movimientos_inventario", back_populates="producto")
    garantias = relationship("Garantias", back_populates="producto")
    productos_descuentos = relationship("Productos_Descuentos", back_populates="producto", overlaps="descuentos")
    descuentos = relationship("Descuentos", secondary="Productos_Descuentos", back_populates="productos", overlaps="productos_descuentos")
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

