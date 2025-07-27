from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.inventario_schema import (
    InventarioBase,
    InventarioCreate,
    InventarioUpdate,
    InventarioSimple,
    InventarioCompleta
)
from ..DB.Inventario_model import Inventario
from ..DB.Productos_model import Productos
from ..DB.Sucursales_model import Sucursales
from ..DB.Movimientos_inventario_model import Movimientos_inventario
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/inventario",
    tags=["Inventario"]
)

# Obtener todo el inventario con paginación y filtros
@router.get("/", response_model=List[InventarioSimple])
async def get_inventario(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    stock_bajo: Optional[bool] = Query(None, description="Filtrar productos con stock bajo"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre o código de producto"),
    ordenar_por: Optional[str] = Query(None, description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Inventario,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Sucursales.Nombre.label('nombre_sucursal')
    ).join(Productos).join(Sucursales)
    
    # Aplicar filtros
    if sucursal_id:
        query = query.filter(Inventario.ID_Sucursal == sucursal_id)
    if stock_bajo is not None:
        if stock_bajo:
            query = query.filter(Inventario.Stock_Actual <= Inventario.Stock_Minimo)
        else:
            query = query.filter(Inventario.Stock_Actual > Inventario.Stock_Minimo)
    if activo is not None:
        query = query.filter(Inventario.Activo == activo)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Productos.Nombre.ilike(search)) |
            (Productos.Codigo_Barras.ilike(search)) |
            (Productos.SKU.ilike(search))
        )
    
    # Aplicar ordenamiento
    if ordenar_por:
        orden_col = getattr(Inventario, ordenar_por.capitalize(), Inventario.ID_Inventario)
        if orden == "desc":
            orden_col = orden_col.desc()
        query = query.order_by(orden_col)
    
    total = query.count()
    inventario = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_inventario": item.Inventario.ID_Inventario,
                "producto": {
                    "id": item.Inventario.ID_Producto,
                    "nombre": item.nombre_producto,
                    "codigo_barras": item.Codigo_Barras
                },
                "sucursal": {
                    "id": item.Inventario.ID_Sucursal,
                    "nombre": item.nombre_sucursal
                },
                "stock_actual": item.Inventario.Stock_Actual,
                "stock_minimo": item.Inventario.Stock_Minimo,
                "stock_maximo": item.Inventario.Stock_Maximo,
                "ubicacion": item.Inventario.Ubicacion,
                "estado": "Bajo" if item.Inventario.Stock_Actual <= item.Inventario.Stock_Minimo
                         else "Alto" if item.Inventario.Stock_Actual >= item.Inventario.Stock_Maximo
                         else "Normal"
            }
            for item in inventario
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener inventario por ID
@router.get("/{inventario_id}", response_model=InventarioCompleta)
async def get_inventario_by_id(
    inventario_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    inventario = db.query(Inventario).filter(Inventario.ID_Inventario == inventario_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    return inventario

# Crear nuevo registro de inventario
@router.post("/", response_model=InventarioCompleta)
async def create_inventario(
    inventario: InventarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar producto
    producto = db.query(Productos).filter(
        Productos.ID_Producto == inventario.id_producto,
        Productos.Activo == True
    ).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")
    
    # Verificar sucursal
    sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == inventario.id_sucursal,
        Sucursales.Activo == True
    ).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada o inactiva")
    
    # Verificar que no exista ya un registro para este producto en esta sucursal
    existe = db.query(Inventario).filter(
        Inventario.ID_Producto == inventario.id_producto,
        Inventario.ID_Sucursal == inventario.id_sucursal
    ).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un registro de inventario para este producto en esta sucursal"
        )
    
    # Validar niveles de stock
    if inventario.stock_minimo < 0:
        raise HTTPException(status_code=400, detail="El stock mínimo no puede ser negativo")
    if inventario.stock_maximo <= inventario.stock_minimo:
        raise HTTPException(
            status_code=400,
            detail="El stock máximo debe ser mayor al stock mínimo"
        )
    
    # Crear registro
    db_inventario = Inventario(**inventario.dict())
    db.add(db_inventario)
    
    # Registrar movimiento inicial si hay stock
    if inventario.stock_actual > 0:
        movimiento = Movimientos_inventario(
            ID_Producto=inventario.id_producto,
            ID_Sucursal=inventario.id_sucursal,
            Tipo="Ajuste",
            Cantidad=inventario.stock_actual,
            ID_Usuario=current_user.ID_Usuario,
            Observaciones="Stock inicial"
        )
        db.add(movimiento)
    
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

# Actualizar registro de inventario
@router.put("/{inventario_id}", response_model=InventarioCompleta)
async def update_inventario(
    inventario: InventarioUpdate,
    inventario_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_inventario = db.query(Inventario).filter(Inventario.ID_Inventario == inventario_id).first()
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    # Validar niveles de stock
    stock_minimo = inventario.stock_minimo if inventario.stock_minimo is not None else db_inventario.Stock_Minimo
    stock_maximo = inventario.stock_maximo if inventario.stock_maximo is not None else db_inventario.Stock_Maximo
    
    if stock_minimo < 0:
        raise HTTPException(status_code=400, detail="El stock mínimo no puede ser negativo")
    if stock_maximo <= stock_minimo:
        raise HTTPException(
            status_code=400,
            detail="El stock máximo debe ser mayor al stock mínimo"
        )
    
    # Actualizar campos
    for key, value in inventario.dict(exclude_unset=True).items():
        setattr(db_inventario, key.capitalize(), value)
    
    db_inventario.Fecha_Ultimo_Movimiento = datetime.now()
    db.commit()
    db.refresh(db_inventario)
    return db_inventario

# Ajustar stock
@router.post("/{inventario_id}/ajuste")
async def ajustar_stock(
    inventario_id: int = Path(..., gt=0),
    cantidad: int = Query(..., description="Cantidad a ajustar (positiva o negativa)"),
    motivo: str = Query(..., min_length=5, max_length=200, description="Motivo del ajuste"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_inventario = db.query(Inventario).filter(Inventario.ID_Inventario == inventario_id).first()
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    nuevo_stock = db_inventario.Stock_Actual + cantidad
    if nuevo_stock < 0:
        raise HTTPException(status_code=400, detail="El stock no puede ser negativo")
    
    # Registrar movimiento
    movimiento = Movimientos_inventario(
        ID_Producto=db_inventario.ID_Producto,
        ID_Sucursal=db_inventario.ID_Sucursal,
        Tipo="Ajuste",
        Cantidad=cantidad,
        ID_Usuario=current_user.ID_Usuario,
        Observaciones=motivo
    )
    db.add(movimiento)
    
    # Actualizar stock
    db_inventario.Stock_Actual = nuevo_stock
    db_inventario.Fecha_Ultimo_Movimiento = datetime.now()
    db.commit()
    
    return {
        "message": "Stock ajustado correctamente",
        "stock_anterior": db_inventario.Stock_Actual - cantidad,
        "ajuste": cantidad,
        "stock_actual": db_inventario.Stock_Actual
    }

# Obtener movimientos de un producto en una sucursal
@router.get("/{inventario_id}/movimientos", response_model=List[dict])
async def get_movimientos_inventario(
    inventario_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    tipo: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    db_inventario = db.query(Inventario).filter(Inventario.ID_Inventario == inventario_id).first()
    if not db_inventario:
        raise HTTPException(status_code=404, detail="Inventario no encontrado")
    
    query = db.query(
        Movimientos_inventario,
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(Usuarios).filter(
        Movimientos_inventario.ID_Producto == db_inventario.ID_Producto,
        Movimientos_inventario.ID_Sucursal == db_inventario.ID_Sucursal
    )
    
    if desde:
        query = query.filter(Movimientos_inventario.Fecha >= desde)
    if hasta:
        query = query.filter(Movimientos_inventario.Fecha <= hasta)
    if tipo:
        query = query.filter(Movimientos_inventario.Tipo == tipo)
    
    movimientos = query.order_by(Movimientos_inventario.Fecha.desc()).all()
    
    return [
        {
            "id": m.Movimientos_inventario.ID_Movimiento,
            "fecha": m.Movimientos_inventario.Fecha,
            "tipo": m.Movimientos_inventario.Tipo,
            "cantidad": m.Movimientos_inventario.Cantidad,
            "usuario": f"{m.nombre_usuario} {m.apellido_usuario}",
            "referencia": {
                "tipo": m.Movimientos_inventario.Tipo_Referencia,
                "id": m.Movimientos_inventario.ID_Referencia
            } if m.Movimientos_inventario.ID_Referencia else None,
            "observaciones": m.Movimientos_inventario.Observaciones
        }
        for m in movimientos
    ]

# Obtener resumen de stock por sucursal
@router.get("/sucursal/{sucursal_id}/resumen", response_model=dict)
async def get_resumen_sucursal(
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == sucursal_id,
        Sucursales.Activo == True
    ).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada o inactiva")
    
    # Estadísticas generales
    stats = db.query(
        func.count(Inventario.ID_Inventario).label('total_productos'),
        func.sum(case((Inventario.Stock_Actual <= Inventario.Stock_Minimo, 1), else_=0)).label('productos_stock_bajo'),
        func.sum(case((Inventario.Stock_Actual >= Inventario.Stock_Maximo, 1), else_=0)).label('productos_stock_alto'),
        func.sum(case((Inventario.Stock_Actual == 0, 1), else_=0)).label('productos_sin_stock')
    ).filter(Inventario.ID_Sucursal == sucursal_id).first()
    
    # Últimos movimientos
    ultimos_movimientos = db.query(
        func.count(Movimientos_inventario.ID_Movimiento).label('total'),
        func.sum(case((Movimientos_inventario.Fecha >= datetime.now() - timedelta(days=1), 1), else_=0)).label('ultimo_dia'),
        func.sum(case((Movimientos_inventario.Fecha >= datetime.now() - timedelta(days=7), 1), else_=0)).label('ultima_semana')
    ).filter(
        Movimientos_inventario.ID_Sucursal == sucursal_id
    ).first()
    
    return {
        "sucursal": {
            "id": sucursal.ID_Sucursal,
            "nombre": sucursal.Nombre
        },
        "estadisticas": {
            "total_productos": stats.total_productos or 0,
            "productos_stock_bajo": stats.productos_stock_bajo or 0,
            "productos_stock_alto": stats.productos_stock_alto or 0,
            "productos_sin_stock": stats.productos_sin_stock or 0
        },
        "movimientos": {
            "total": ultimos_movimientos.total or 0,
            "ultimo_dia": ultimos_movimientos.ultimo_dia or 0,
            "ultima_semana": ultimos_movimientos.ultima_semana or 0
        },
        "ultima_actualizacion": datetime.now()
    }
