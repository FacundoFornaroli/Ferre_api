from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Garantias_schema import (
    GarantiaBase,
    GarantiaCreate,
    GarantiaUpdate,
    GarantiaSimple,
    GarantiaCompleta,
    EjecucionGarantia,
    EstadisticasGarantias
)
from ..DB.Garantias_model import Garantias
from ..DB.Productos_model import Productos
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/garantias",
    tags=["Garantías"]
)

# Obtener todas las garantías con paginación y filtros
@router.get("/", response_model=List[GarantiaSimple])
async def get_garantias(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    producto_id: Optional[int] = Query(None, description="Filtrar por producto"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de garantía"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Garantias,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU
    ).join(
        Productos
    )
    
    # Aplicar filtros
    if producto_id:
        query = query.filter(Garantias.ID_Producto == producto_id)
    if tipo:
        query = query.filter(Garantias.Tipo_Garantia == tipo)
    if activo is not None:
        query = query.filter(Garantias.Activo == activo)
    
    total = query.count()
    garantias = query.order_by(Garantias.ID_Garantia).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_garantia": g.Garantias.ID_Garantia,
                "producto": {
                    "id": g.Garantias.ID_Producto,
                    "nombre": g.nombre_producto,
                    "codigo_barras": g.Codigo_Barras,
                    "sku": g.SKU
                },
                "tipo_garantia": g.Garantias.Tipo_Garantia,
                "tiempo_garantia": g.Garantias.Tiempo_Garantia,
                "activo": g.Garantias.Activo
            }
            for g in garantias
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una garantía específica
@router.get("/{garantia_id}", response_model=GarantiaCompleta)
async def get_garantia(
    garantia_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    garantia = db.query(
        Garantias,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU,
        Productos.Marca
    ).join(
        Productos
    ).filter(
        Garantias.ID_Garantia == garantia_id
    ).first()
    
    if not garantia:
        raise HTTPException(status_code=404, detail="Garantía no encontrada")
    
    # Obtener cantidad de productos vendidos con esta garantía
    productos_vendidos = db.query(
        func.count(Detalles_Factura_Venta.ID_Detalle).label('total_ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('total_unidades')
    ).join(
        Facturas_Venta,
        and_(
            Detalles_Factura_Venta.ID_Factura_Venta == Facturas_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada'
        )
    ).filter(
        Detalles_Factura_Venta.ID_Producto == garantia.Garantias.ID_Producto,
        Facturas_Venta.Fecha >= datetime.now() - timedelta(days=garantia.Garantias.Tiempo_Garantia)
    ).first()
    
    return {
        "garantia": {
            "id_garantia": garantia.Garantias.ID_Garantia,
            "producto": {
                "id": garantia.Garantias.ID_Producto,
                "nombre": garantia.nombre_producto,
                "codigo_barras": garantia.Codigo_Barras,
                "sku": garantia.SKU,
                "marca": garantia.Marca
            },
            "tipo_garantia": garantia.Garantias.Tipo_Garantia,
            "tiempo_garantia": garantia.Garantias.Tiempo_Garantia,
            "descripcion": garantia.Garantias.Descripcion,
            "activo": garantia.Garantias.Activo
        },
        "estadisticas": {
            "productos_en_garantia": {
                "ventas": productos_vendidos.total_ventas or 0,
                "unidades": productos_vendidos.total_unidades or 0
            },
            "fecha_ejemplo": {
                "compra": datetime.now(),
                "vencimiento": datetime.now() + timedelta(days=garantia.Garantias.Tiempo_Garantia)
            }
        }
    }

# Crear nueva garantía
@router.post("/", response_model=GarantiaCompleta)
async def create_garantia(
    garantia: GarantiaCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar producto
    producto = db.query(Productos).filter(
        Productos.ID_Producto == garantia.id_producto,
        Productos.Activo == True
    ).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado o inactivo")
    
    # Verificar si ya existe garantía activa para este producto
    existe_garantia = db.query(Garantias).filter(
        Garantias.ID_Producto == garantia.id_producto,
        Garantias.Activo == True
    ).first()
    if existe_garantia:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una garantía activa para este producto"
        )
    
    # Validar tiempo de garantía
    if garantia.tiempo_garantia <= 0:
        raise HTTPException(
            status_code=400,
            detail="El tiempo de garantía debe ser mayor a 0 días"
        )
    
    # Crear garantía
    db_garantia = Garantias(
        ID_Producto=garantia.id_producto,
        Tipo_Garantia=garantia.tipo_garantia,
        Tiempo_Garantia=garantia.tiempo_garantia,
        Descripcion=garantia.descripcion
    )
    db.add(db_garantia)
    db.commit()
    db.refresh(db_garantia)
    
    return await get_garantia(db_garantia.ID_Garantia, db, current_user)

# Actualizar garantía
@router.put("/{garantia_id}", response_model=GarantiaCompleta)
async def update_garantia(
    garantia: GarantiaUpdate,
    garantia_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_garantia = db.query(Garantias).filter(Garantias.ID_Garantia == garantia_id).first()
    if not db_garantia:
        raise HTTPException(status_code=404, detail="Garantía no encontrada")
    
    # Validar tiempo de garantía
    if garantia.tiempo_garantia is not None and garantia.tiempo_garantia <= 0:
        raise HTTPException(
            status_code=400,
            detail="El tiempo de garantía debe ser mayor a 0 días"
        )
    
    # Actualizar campos
    for key, value in garantia.dict(exclude_unset=True).items():
        setattr(db_garantia, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_garantia)
    
    return await get_garantia(garantia_id, db, current_user)

# Verificar garantía de un producto vendido
@router.get("/verificar/{factura_id}/{producto_id}", response_model=dict)
async def verificar_garantia(
    factura_id: int = Path(..., gt=0),
    producto_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar venta
    venta = db.query(
        Detalles_Factura_Venta,
        Facturas_Venta.Fecha.label('fecha_venta'),
        Facturas_Venta.Estado.label('estado_factura')
    ).join(
        Facturas_Venta
    ).filter(
        Detalles_Factura_Venta.ID_Factura_Venta == factura_id,
        Detalles_Factura_Venta.ID_Producto == producto_id
    ).first()
    
    if not venta:
        raise HTTPException(
            status_code=404,
            detail="No se encontró el producto en la factura especificada"
        )
    
    if venta.estado_factura == "Anulada":
        raise HTTPException(
            status_code=400,
            detail="La factura está anulada"
        )
    
    # Verificar garantía
    garantia = db.query(Garantias).filter(
        Garantias.ID_Producto == producto_id,
        Garantias.Activo == True
    ).first()
    
    if not garantia:
        return {
            "tiene_garantia": False,
            "mensaje": "El producto no tiene garantía"
        }
    
    # Calcular fechas
    fecha_venta = venta.fecha_venta
    fecha_vencimiento = fecha_venta + timedelta(days=garantia.Tiempo_Garantia)
    dias_restantes = (fecha_vencimiento - datetime.now()).days
    
    return {
        "tiene_garantia": True,
        "estado": "Vigente" if dias_restantes > 0 else "Vencida",
        "garantia": {
            "tipo": garantia.Tipo_Garantia,
            "tiempo_total_dias": garantia.Tiempo_Garantia,
            "descripcion": garantia.Descripcion
        },
        "fechas": {
            "venta": fecha_venta,
            "vencimiento": fecha_vencimiento,
            "dias_restantes": max(0, dias_restantes)
        }
    }

# Obtener estadísticas de garantías
@router.get("/estadisticas", response_model=EstadisticasGarantias)
async def get_estadisticas_garantias(
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Garantías por tipo
    por_tipo = db.query(
        Garantias.Tipo_Garantia,
        func.count(Garantias.ID_Garantia).label('total'),
        func.avg(Garantias.Tiempo_Garantia).label('tiempo_promedio')
    ).group_by(
        Garantias.Tipo_Garantia
    ).all()
    
    # Productos con más ventas en garantía
    productos_garantia = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        Garantias.Tipo_Garantia,
        Garantias.Tiempo_Garantia,
        func.count(Detalles_Factura_Venta.ID_Detalle).label('total_ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('total_unidades')
    ).join(
        Garantias,
        and_(
            Garantias.ID_Producto == Productos.ID_Producto,
            Garantias.Activo == True
        )
    ).join(
        Detalles_Factura_Venta,
        Detalles_Factura_Venta.ID_Producto == Productos.ID_Producto
    ).join(
        Facturas_Venta,
        and_(
            Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada',
            Facturas_Venta.Fecha >= datetime.now() - timedelta(days=365)
        )
    ).group_by(
        Productos.ID_Producto,
        Productos.Nombre,
        Garantias.Tipo_Garantia,
        Garantias.Tiempo_Garantia
    ).order_by(
        func.count(Detalles_Factura_Venta.ID_Detalle).desc()
    ).limit(10).all()
    
    return {
        "por_tipo": [
            {
                "tipo": t.Tipo_Garantia,
                "total": t.total,
                "tiempo_promedio_dias": round(t.tiempo_promedio, 1)
            }
            for t in por_tipo
        ],
        "productos_mas_vendidos": [
            {
                "producto": {
                    "id": p.ID_Producto,
                    "nombre": p.Nombre
                },
                "garantia": {
                    "tipo": p.Tipo_Garantia,
                    "tiempo_dias": p.Tiempo_Garantia
                },
                "ventas": {
                    "total_ventas": p.total_ventas,
                    "total_unidades": p.total_unidades
                }
            }
            for p in productos_garantia
        ],
        "resumen": {
            "total_garantias_activas": sum(t.total for t in por_tipo),
            "tiempo_promedio_general": round(
                sum(t.tiempo_promedio * t.total for t in por_tipo) / 
                sum(t.total for t in por_tipo)
                if sum(t.total for t in por_tipo) > 0 else 0,
                1
            )
        }
    }
