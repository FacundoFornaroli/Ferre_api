from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Movimientos_Inventario_schema import (
    MovimientoInventarioBase,
    MovimientoInventarioCreate,
    MovimientoInventarioUpdate,
    MovimientoInventarioSimple,
    MovimientoInventarioCompleto,
    AnalisisMovimientos
)
from ..DB.Movimientos_inventario_model import Movimientos_inventario
from ..DB.Productos_model import Productos
from ..DB.Sucursales_model import Sucursales
from ..DB.Inventario_model import Inventario
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/movimientos-inventario",
    tags=["Movimientos de Inventario"]
)

# Obtener movimientos con paginación y filtros
@router.get("/", response_model=List[MovimientoInventarioSimple])
async def get_movimientos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de movimiento"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Movimientos_inventario,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Sucursales.Nombre.label('nombre_sucursal'),
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Productos
    ).join(
        Sucursales
    ).join(
        Usuarios
    )
    
    # Aplicar filtros
    if producto_id:
        query = query.filter(Movimientos_inventario.ID_Producto == producto_id)
    if sucursal_id:
        query = query.filter(Movimientos_inventario.ID_Sucursal == sucursal_id)
    if tipo:
        query = query.filter(Movimientos_inventario.Tipo == tipo)
    if desde:
        query = query.filter(Movimientos_inventario.Fecha >= desde)
    if hasta:
        query = query.filter(Movimientos_inventario.Fecha <= hasta)
    
    total = query.count()
    movimientos = query.order_by(Movimientos_inventario.Fecha.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_movimiento": m.Movimientos_inventario.ID_Movimiento,
                "fecha": m.Movimientos_inventario.Fecha,
                "tipo": m.Movimientos_inventario.Tipo,
                "producto": {
                    "id": m.Movimientos_inventario.ID_Producto,
                    "nombre": m.nombre_producto,
                    "codigo_barras": m.Codigo_Barras
                },
                "sucursal": {
                    "id": m.Movimientos_inventario.ID_Sucursal,
                    "nombre": m.nombre_sucursal
                },
                "cantidad": m.Movimientos_inventario.Cantidad,
                "usuario": f"{m.nombre_usuario} {m.apellido_usuario}",
                "referencia": {
                    "tipo": m.Movimientos_inventario.Tipo_Referencia,
                    "id": m.Movimientos_inventario.ID_Referencia
                } if m.Movimientos_inventario.ID_Referencia else None
            }
            for m in movimientos
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener un movimiento específico
@router.get("/{movimiento_id}", response_model=MovimientoInventarioCompleto)
async def get_movimiento(
    movimiento_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    movimiento = db.query(
        Movimientos_inventario,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU,
        Sucursales.Nombre.label('nombre_sucursal'),
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Productos
    ).join(
        Sucursales
    ).join(
        Usuarios
    ).filter(
        Movimientos_inventario.ID_Movimiento == movimiento_id
    ).first()
    
    if not movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    
    # Obtener stock antes y después del movimiento
    stock_anterior = db.query(
        func.sum(case(
            (Movimientos_inventario.Fecha < movimiento.Movimientos_inventario.Fecha, Movimientos_inventario.Cantidad),
            else_=0
        ))
    ).filter(
        Movimientos_inventario.ID_Producto == movimiento.Movimientos_inventario.ID_Producto,
        Movimientos_inventario.ID_Sucursal == movimiento.Movimientos_inventario.ID_Sucursal
    ).scalar() or 0
    
    return {
        "movimiento": {
            "id_movimiento": movimiento.Movimientos_inventario.ID_Movimiento,
            "fecha": movimiento.Movimientos_inventario.Fecha,
            "tipo": movimiento.Movimientos_inventario.Tipo,
            "producto": {
                "id": movimiento.Movimientos_inventario.ID_Producto,
                "nombre": movimiento.nombre_producto,
                "codigo_barras": movimiento.Codigo_Barras,
                "sku": movimiento.SKU
            },
            "sucursal": {
                "id": movimiento.Movimientos_inventario.ID_Sucursal,
                "nombre": movimiento.nombre_sucursal
            },
            "cantidad": movimiento.Movimientos_inventario.Cantidad,
            "costo_unitario": movimiento.Movimientos_inventario.Costo_Unitario,
            "usuario": {
                "id": movimiento.Movimientos_inventario.ID_Usuario,
                "nombre": f"{movimiento.nombre_usuario} {movimiento.apellido_usuario}"
            },
            "referencia": {
                "tipo": movimiento.Movimientos_inventario.Tipo_Referencia,
                "id": movimiento.Movimientos_inventario.ID_Referencia
            } if movimiento.Movimientos_inventario.ID_Referencia else None,
            "observaciones": movimiento.Movimientos_inventario.Observaciones
        },
        "analisis": {
            "stock_anterior": stock_anterior,
            "stock_posterior": stock_anterior + movimiento.Movimientos_inventario.Cantidad
        }
    }

# Registrar nuevo movimiento manual
@router.post("/", response_model=MovimientoInventarioCompleto)
async def create_movimiento(
    movimiento: MovimientoInventarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar producto
    producto = db.query(Productos).filter(
        Productos.ID_Producto == movimiento.id_producto,
        Productos.Activo == True
    ).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")
    
    # Verificar sucursal
    sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == movimiento.id_sucursal,
        Sucursales.Activo == True
    ).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada o inactiva")
    
    # Verificar inventario
    inventario = db.query(Inventario).filter(
        Inventario.ID_Producto == movimiento.id_producto,
        Inventario.ID_Sucursal == movimiento.id_sucursal
    ).first()
    
    if not inventario:
        inventario = Inventario(
            ID_Producto=movimiento.id_producto,
            ID_Sucursal=movimiento.id_sucursal,
            Stock_Actual=0,
            Stock_Minimo=0,
            Stock_Maximo=999999
        )
        db.add(inventario)
        db.flush()
    
    # Validar stock si es salida
    if movimiento.tipo in ["Venta", "Transferencia", "Ajuste"] and movimiento.cantidad < 0:
        if abs(movimiento.cantidad) > inventario.Stock_Actual:
            raise HTTPException(
                status_code=400,
                detail="Stock insuficiente para realizar el movimiento"
            )
    
    # Crear movimiento
    db_movimiento = Movimientos_inventario(
        ID_Producto=movimiento.id_producto,
        ID_Sucursal=movimiento.id_sucursal,
        Tipo=movimiento.tipo,
        Cantidad=movimiento.cantidad,
        Costo_Unitario=movimiento.costo_unitario,
        ID_Usuario=current_user.ID_Usuario,
        ID_Referencia=movimiento.id_referencia,
        Tipo_Referencia=movimiento.tipo_referencia,
        Observaciones=movimiento.observaciones
    )
    db.add(db_movimiento)
    
    # Actualizar stock
    inventario.Stock_Actual += movimiento.cantidad
    inventario.Fecha_Ultimo_Movimiento = datetime.now()
    
    db.commit()
    db.refresh(db_movimiento)
    
    return await get_movimiento(db_movimiento.ID_Movimiento, db, current_user)

# Obtener análisis de movimientos por producto
@router.get("/producto/{producto_id}/analisis", response_model=AnalisisMovimientos)
async def get_analisis_movimientos(
    producto_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar producto
    producto = db.query(Productos).filter(Productos.ID_Producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    query = db.query(Movimientos_inventario)
    if desde:
        query = query.filter(Movimientos_inventario.Fecha >= desde)
    if hasta:
        query = query.filter(Movimientos_inventario.Fecha <= hasta)
    
    # Análisis por tipo de movimiento
    por_tipo = db.query(
        Movimientos_inventario.Tipo,
        func.count(Movimientos_inventario.ID_Movimiento).label('cantidad_movimientos'),
        func.sum(Movimientos_inventario.Cantidad).label('cantidad_total')
    ).filter(
        Movimientos_inventario.ID_Producto == producto_id,
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(
        Movimientos_inventario.Tipo
    ).all()
    
    # Stock por sucursal
    stock_sucursales = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Inventario.Stock_Actual,
        Inventario.Stock_Minimo,
        Inventario.Stock_Maximo
    ).join(
        Inventario,
        and_(
            Inventario.ID_Sucursal == Sucursales.ID_Sucursal,
            Inventario.ID_Producto == producto_id
        )
    ).filter(
        Inventario.Stock_Actual > 0
    ).all()
    
    # Últimos movimientos
    ultimos_movimientos = db.query(
        Movimientos_inventario,
        Sucursales.Nombre.label('nombre_sucursal')
    ).join(
        Sucursales
    ).filter(
        Movimientos_inventario.ID_Producto == producto_id,
        *query.whereclause.clauses if query.whereclause else []
    ).order_by(
        Movimientos_inventario.Fecha.desc()
    ).limit(5).all()
    
    # Calcular rotación
    if desde and hasta:
        dias = (hasta - desde).days
        total_salidas = abs(sum(
            m.cantidad_total for m in por_tipo 
            if m.Tipo in ["Venta", "Transferencia"] and m.cantidad_total < 0
        ))
        stock_promedio = db.query(func.avg(Inventario.Stock_Actual)).filter(
            Inventario.ID_Producto == producto_id
        ).scalar() or 0
        
        rotacion = (total_salidas / stock_promedio) * (365 / dias) if stock_promedio > 0 and dias > 0 else 0
    else:
        rotacion = 0
    
    return {
        "producto": {
            "id": producto.ID_Producto,
            "nombre": producto.Nombre,
            "codigo_barras": producto.Codigo_Barras,
            "sku": producto.SKU
        },
        "movimientos_por_tipo": [
            {
                "tipo": m.Tipo,
                "cantidad_movimientos": m.cantidad_movimientos,
                "cantidad_total": m.cantidad_total
            }
            for m in por_tipo
        ],
        "stock_por_sucursal": [
            {
                "sucursal": {
                    "id": s.ID_Sucursal,
                    "nombre": s.Nombre
                },
                "stock_actual": s.Stock_Actual,
                "stock_minimo": s.Stock_Minimo,
                "stock_maximo": s.Stock_Maximo,
                "estado": "Bajo" if s.Stock_Actual <= s.Stock_Minimo
                         else "Alto" if s.Stock_Actual >= s.Stock_Maximo
                         else "Normal"
            }
            for s in stock_sucursales
        ],
        "ultimos_movimientos": [
            {
                "fecha": m.Movimientos_inventario.Fecha,
                "tipo": m.Movimientos_inventario.Tipo,
                "cantidad": m.Movimientos_inventario.Cantidad,
                "sucursal": m.nombre_sucursal
            }
            for m in ultimos_movimientos
        ],
        "analisis": {
            "rotacion": round(rotacion, 2),
            "periodo": {
                "desde": desde,
                "hasta": hasta
            }
        }
    }