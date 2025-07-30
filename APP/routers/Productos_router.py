from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Productos_schema import (
    ProductoBase,
    ProductoCreate,
    ProductoUpdate,
    ProductoSimple,
    ProductoCompleta
)
from APP.DB.Productos_model import Productos
from APP.DB.Categorias_model import Categorias
from APP.DB.Unidades_de_medida_model import Unidades_de_medida
from APP.DB.Inventario_model import Inventario
from APP.DB.Garantias_model import Garantias
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# Obtener todos los productos con paginación y filtros
@router.get("/", response_model=List[ProductoSimple])
async def get_productos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    marca: Optional[str] = Query(None, description="Filtrar por marca"),
    precio_min: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    precio_max: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    con_stock: Optional[bool] = Query(None, description="Filtrar productos con stock"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, código o descripción"),
    ordenar_por: Optional[str] = Query(None, description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    query = db.query(Productos)
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Productos.Activo == activo)
    if categoria_id:
        query = query.filter(Productos.ID_Categoria == categoria_id)
    if marca:
        query = query.filter(Productos.Marca.ilike(f"%{marca}%"))
    if precio_min:
        query = query.filter(Productos.Precio >= precio_min)
    if precio_max:
        query = query.filter(Productos.Precio <= precio_max)
    if con_stock is not None:
        query = query.join(Inventario).group_by(Productos.ID_Producto)
        if con_stock:
            query = query.having(func.sum(Inventario.Stock_Actual) > 0)
        else:
            query = query.having(func.sum(Inventario.Stock_Actual) == 0)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Productos.Nombre.ilike(search)) |
            (Productos.Codigo_Barras.ilike(search)) |
            (Productos.SKU.ilike(search)) |
            (Productos.Descripcion.ilike(search))
        )
    
    # Aplicar ordenamiento
    if ordenar_por:
        orden_col = getattr(Productos, ordenar_por.capitalize(), Productos.Nombre)
        if orden == "desc":
            orden_col = orden_col.desc()
        query = query.order_by(orden_col)
    
    total = query.count()
    productos = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": productos,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Buscar productos por código de barras
@router.get("/buscar/{codigo}", response_model=ProductoSimple)
async def buscar_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    producto = db.query(Productos).filter(
        (Productos.Codigo_Barras == codigo) |
        (Productos.SKU == codigo)
    ).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Obtener productos con stock bajo
@router.get("/reportes/stock-bajo", response_model=List[dict])
async def get_productos_stock_bajo(
    limite: int = Query(10, ge=1, le=100),
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        Productos.Codigo_Barras,
        Inventario.ID_Sucursal,
        Inventario.Stock_Actual,
        Inventario.Stock_Minimo
    ).join(Inventario).filter(
        Inventario.Stock_Actual <= Inventario.Stock_Minimo
    )
    
    if sucursal_id:
        query = query.filter(Inventario.ID_Sucursal == sucursal_id)
    
    productos = query.limit(limite).all()
    
    return [
        {
            "id": p.ID_Producto,
            "nombre": p.Nombre,
            "codigo_barras": p.Codigo_Barras,
            "sucursal_id": p.ID_Sucursal,
            "stock_actual": p.Stock_Actual,
            "stock_minimo": p.Stock_Minimo,
            "faltante": p.Stock_Minimo - p.Stock_Actual
        }
        for p in productos
    ]

# Obtener un producto por ID
@router.get("/{producto_id}", response_model=ProductoCompleta)
async def get_producto(
    producto_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Crear nuevo producto
@router.post("/", response_model=ProductoCompleta)
async def create_producto(
    producto: ProductoCreate,
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar códigos únicos
    if producto.codigo_barras:
        existe_codigo = db.query(Productos).filter(
            Productos.Codigo_Barras == producto.codigo_barras
        ).first()
        if existe_codigo:
            raise HTTPException(status_code=400, detail="Código de barras ya registrado")
    
    if producto.sku:
        existe_sku = db.query(Productos).filter(
            Productos.SKU == producto.sku
        ).first()
        if existe_sku:
            raise HTTPException(status_code=400, detail="SKU ya registrado")
    
    # Verificar categoría
    categoria = db.query(Categorias).filter(
        Categorias.ID_Categoria == producto.id_categoria,
        Categorias.Activo == True
    ).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o inactiva")
    
    # Verificar unidad de medida
    unidad = db.query(Unidades_de_medida).filter(
        Unidades_de_medida.ID_Unidad_de_medida == producto.id_unidad_de_medida,
        Unidades_de_medida.Activo == True
    ).first()
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad de medida no encontrada o inactiva")
    
    # Validar precios
    if producto.precio_mayorista and producto.precio_mayorista >= producto.precio:
        raise HTTPException(
            status_code=400,
            detail="El precio mayorista debe ser menor al precio regular"
        )
    
    if producto.precio <= producto.costo:
        raise HTTPException(
            status_code=400,
            detail="El precio debe ser mayor al costo"
        )
    
    # Crear producto
    db_producto = Productos(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Actualizar producto
@router.put("/{producto_id}", response_model=ProductoCompleta)
async def update_producto(
    producto: ProductoUpdate,
    producto_id: int = Path(..., gt=0),
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Verificar códigos únicos
    if producto.codigo_barras and producto.codigo_barras != db_producto.Codigo_Barras:
        existe_codigo = db.query(Productos).filter(
            Productos.Codigo_Barras == producto.codigo_barras,
            Productos.ID_Producto != producto_id
        ).first()
        if existe_codigo:
            raise HTTPException(status_code=400, detail="Código de barras ya registrado")
    
    if producto.sku and producto.sku != db_producto.SKU:
        existe_sku = db.query(Productos).filter(
            Productos.SKU == producto.sku,
            Productos.ID_Producto != producto_id
        ).first()
        if existe_sku:
            raise HTTPException(status_code=400, detail="SKU ya registrado")
    
    # Verificar categoría
    if producto.id_categoria:
        categoria = db.query(Categorias).filter(
            Categorias.ID_Categoria == producto.id_categoria,
            Categorias.Activo == True
        ).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoría no encontrada o inactiva")
    
    # Verificar unidad de medida
    if producto.id_unidad_de_medida:
        unidad = db.query(Unidades_de_medida).filter(
            Unidades_de_medida.ID_Unidad_de_medida == producto.id_unidad_de_medida,
            Unidades_de_medida.Activo == True
        ).first()
        if not unidad:
            raise HTTPException(status_code=404, detail="Unidad de medida no encontrada o inactiva")
    
    # Validar precios
    precio = producto.precio if producto.precio is not None else db_producto.Precio
    costo = producto.costo if producto.costo is not None else db_producto.Costo
    precio_mayorista = producto.precio_mayorista if producto.precio_mayorista is not None else db_producto.Precio_Mayorista
    
    if precio_mayorista and precio_mayorista >= precio:
        raise HTTPException(
            status_code=400,
            detail="El precio mayorista debe ser menor al precio regular"
        )
    
    if precio <= costo:
        raise HTTPException(
            status_code=400,
            detail="El precio debe ser mayor al costo"
        )
    
    # Actualizar campos
    for key, value in producto.dict(exclude_unset=True).items():
        setattr(db_producto, key.capitalize(), value)
    
    db_producto.Fecha_Actualizacion = datetime.now()
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Obtener stock por sucursal
@router.get("/{producto_id}/stock", response_model=List[dict])
async def get_stock_por_sucursal(
    producto_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    stocks = db.query(
        Inventario.ID_Sucursal,
        Inventario.Stock_Actual,
        Inventario.Stock_Minimo,
        Inventario.Stock_Maximo,
        Inventario.Ubicacion
    ).filter(Inventario.ID_Producto == producto_id).all()
    
    return [
        {
            "sucursal_id": s.ID_Sucursal,
            "stock_actual": s.Stock_Actual,
            "stock_minimo": s.Stock_Minimo,
            "stock_maximo": s.Stock_Maximo,
            "ubicacion": s.Ubicacion,
            "estado": "Bajo" if s.Stock_Actual <= s.Stock_Minimo else "Alto" if s.Stock_Actual >= s.Stock_Maximo else "Normal"
        }
        for s in stocks
    ]

# Obtener historial de precios
@router.get("/{producto_id}/historial-precios", response_model=List[dict])
async def get_historial_precios(
    producto_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    # Esta función requiere una tabla de historial de precios
    # Por ahora retornamos un ejemplo
    return [
        {
            "fecha": datetime.now() - timedelta(days=30),
            "precio": 100.00,
            "precio_mayorista": 90.00,
            "usuario": "Sistema"
        }
    ]

# Obtener estadísticas del producto
@router.get("/{producto_id}/estadisticas", response_model=dict)
async def get_estadisticas_producto(
    producto_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # Stock total
    stock_total = db.query(func.sum(Inventario.Stock_Actual)).filter(
        Inventario.ID_Producto == producto_id
    ).scalar() or 0
    
    # Sucursales con stock bajo
    stock_bajo = db.query(func.count()).filter(
        Inventario.ID_Producto == producto_id,
        Inventario.Stock_Actual <= Inventario.Stock_Minimo
    ).scalar() or 0
    
    # Garantía
    garantia = db.query(Garantias).filter(
        Garantias.ID_Producto == producto_id,
        Garantias.Activo == True
    ).first()
    
    return {
        "stock_total": stock_total,
        "sucursales_stock_bajo": stock_bajo,
        "tiene_garantia": bool(garantia),
        "tiempo_garantia": garantia.Tiempo_Garantia if garantia else None,
        "ultima_actualizacion": producto.Fecha_Actualizacion,
        "margen_ganancia": ((producto.Precio - producto.Costo) / producto.Costo * 100)
        if producto.Costo > 0 else 0
    }

# Buscar productos por código de barras
@router.get("/buscar/{codigo}", response_model=ProductoSimple)
async def buscar_por_codigo(
    codigo: str,
    db: Session = Depends(get_db)
):
    producto = db.query(Productos).filter(
        (Productos.Codigo_Barras == codigo) |
        (Productos.SKU == codigo)
    ).first()
    
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Obtener productos con stock bajo
@router.get("/reportes/stock-bajo", response_model=List[dict])
async def get_productos_stock_bajo(
    limite: int = Query(10, ge=1, le=100),
    sucursal_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        Productos.Codigo_Barras,
        Inventario.ID_Sucursal,
        Inventario.Stock_Actual,
        Inventario.Stock_Minimo
    ).join(Inventario).filter(
        Inventario.Stock_Actual <= Inventario.Stock_Minimo
    )
    
    if sucursal_id:
        query = query.filter(Inventario.ID_Sucursal == sucursal_id)
    
    productos = query.limit(limite).all()
    
    return [
        {
            "id": p.ID_Producto,
            "nombre": p.Nombre,
            "codigo_barras": p.Codigo_Barras,
            "sucursal_id": p.ID_Sucursal,
            "stock_actual": p.Stock_Actual,
            "stock_minimo": p.Stock_Minimo,
            "faltante": p.Stock_Minimo - p.Stock_Actual
        }
        for p in productos
    ]
