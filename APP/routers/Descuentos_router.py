from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Descuentos_schema import (
    DescuentoBase,
    DescuentoCreate,
    DescuentoUpdate,
    DescuentoSimple,
    DescuentoCompleto,
    ProductoDescuentoBase,
    EstadisticasDescuentos
)
from ..DB.Descuentos_model import Descuentos
from ..DB.Productos_Descuentos_model import Productos_Descuentos
from ..DB.Productos_model import Productos
from ..DB.Detalles_Factura_Venta_model import Detalles_Factura_Venta
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/descuentos",
    tags=["Descuentos"]
)

# Obtener todos los descuentos con paginación y filtros
@router.get("/", response_model=List[DescuentoSimple])
async def get_descuentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    tipo: Optional[str] = Query(None, description="Filtrar por tipo de descuento"),
    vigente: Optional[bool] = Query(None, description="Filtrar por vigencia actual"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(Descuentos)
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Descuentos.Activo == activo)
    if tipo:
        query = query.filter(Descuentos.Tipo_Descuento == tipo)
    if vigente is not None:
        hoy = datetime.now().date()
        if vigente:
            query = query.filter(
                Descuentos.Fecha_Inicio <= hoy,
                Descuentos.Fecha_Fin >= hoy,
                Descuentos.Activo == True
            )
        else:
            query = query.filter(
                Descuentos.Fecha_Fin < hoy
            )
    
    total = query.count()
    descuentos = query.order_by(Descuentos.Fecha_Inicio.desc()).offset(skip).limit(limit).all()
    
    # Obtener cantidad de productos por descuento
    resultados = []
    for descuento in descuentos:
        productos_count = db.query(func.count(Productos_Descuentos.ID_Producto)).filter(
            Productos_Descuentos.ID_Descuento == descuento.ID_Descuento
        ).scalar()
        
        # Calcular estado de vigencia
        hoy = datetime.now().date()
        if not descuento.Activo:
            estado = "Inactivo"
        elif descuento.Fecha_Inicio > hoy:
            estado = "Pendiente"
        elif descuento.Fecha_Fin < hoy:
            estado = "Vencido"
        else:
            estado = "Vigente"
        
        resultados.append({
            "id_descuento": descuento.ID_Descuento,
            "nombre": descuento.Nombre,
            "tipo_descuento": descuento.Tipo_Descuento,
            "porcentaje": descuento.Porcentaje,
            "monto_fijo": descuento.Monto_Fijo,
            "fecha_inicio": descuento.Fecha_Inicio,
            "fecha_fin": descuento.Fecha_Fin,
            "estado": estado,
            "productos_count": productos_count
        })
    
    return {
        "total": total,
        "items": resultados,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener un descuento específico con sus productos
@router.get("/{descuento_id}", response_model=DescuentoCompleto)
async def get_descuento(
    descuento_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    descuento = db.query(Descuentos).filter(Descuentos.ID_Descuento == descuento_id).first()
    if not descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    
    # Obtener productos asociados
    productos = db.query(
        Productos,
        Productos_Descuentos
    ).join(
        Productos_Descuentos,
        Productos_Descuentos.ID_Producto == Productos.ID_Producto
    ).filter(
        Productos_Descuentos.ID_Descuento == descuento_id
    ).all()
    
    # Calcular efectividad del descuento
    ventas_con_descuento = db.query(
        func.count(Detalles_Factura_Venta.ID_Detalle).label('cantidad_ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('unidades_vendidas'),
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
    ).join(
        Facturas_Venta,
        and_(
            Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada',
            Facturas_Venta.Fecha.between(descuento.Fecha_Inicio, descuento.Fecha_Fin)
        )
    ).join(
        Productos_Descuentos,
        and_(
            Productos_Descuentos.ID_Producto == Detalles_Factura_Venta.ID_Producto,
            Productos_Descuentos.ID_Descuento == descuento_id
        )
    ).first()
    
    return {
        "descuento": {
            "id_descuento": descuento.ID_Descuento,
            "nombre": descuento.Nombre,
            "descripcion": descuento.Descripcion,
            "tipo_descuento": descuento.Tipo_Descuento,
            "porcentaje": descuento.Porcentaje,
            "monto_fijo": descuento.Monto_Fijo,
            "fecha_inicio": descuento.Fecha_Inicio,
            "fecha_fin": descuento.Fecha_Fin,
            "cantidad_minima": descuento.Cantidad_Minima,
            "cantidad_maxima": descuento.Cantidad_Maxima,
            "activo": descuento.Activo
        },
        "productos": [
            {
                "id_producto": p.Productos.ID_Producto,
                "nombre": p.Productos.Nombre,
                "codigo_barras": p.Productos.Codigo_Barras,
                "precio": p.Productos.Precio,
                "precio_con_descuento": p.Productos.Precio * (1 - descuento.Porcentaje/100)
                if descuento.Tipo_Descuento == "Porcentaje"
                else p.Productos.Precio - descuento.Monto_Fijo
            }
            for p in productos
        ],
        "estadisticas": {
            "ventas": ventas_con_descuento.cantidad_ventas or 0,
            "unidades": ventas_con_descuento.unidades_vendidas or 0,
            "total_descuento": ventas_con_descuento.total_descuento or 0,
            "dias_restantes": (descuento.Fecha_Fin - datetime.now().date()).days
            if descuento.Fecha_Fin >= datetime.now().date() else 0
        }
    }

# Crear nuevo descuento
@router.post("/", response_model=DescuentoCompleto)
async def create_descuento(
    descuento: DescuentoCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Validaciones
    if descuento.fecha_inicio >= descuento.fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin debe ser posterior a la fecha de inicio"
        )
    
    if descuento.tipo_descuento == "Porcentaje":
        if not 0 < descuento.porcentaje <= 100:
            raise HTTPException(
                status_code=400,
                detail="El porcentaje debe estar entre 0 y 100"
            )
    elif descuento.tipo_descuento == "Monto Fijo":
        if not descuento.monto_fijo or descuento.monto_fijo <= 0:
            raise HTTPException(
                status_code=400,
                detail="El monto fijo debe ser mayor a 0"
            )
    
    if descuento.cantidad_maxima and descuento.cantidad_minima and descuento.cantidad_maxima <= descuento.cantidad_minima:
        raise HTTPException(
            status_code=400,
            detail="La cantidad máxima debe ser mayor a la cantidad mínima"
        )
    
    # Verificar productos
    if descuento.productos:
        productos_ids = [p.id_producto for p in descuento.productos]
        productos_existentes = db.query(Productos).filter(
            Productos.ID_Producto.in_(productos_ids),
            Productos.Activo == True
        ).all()
        if len(productos_existentes) != len(productos_ids):
            raise HTTPException(
                status_code=400,
                detail="Uno o más productos no existen o están inactivos"
            )
    
    # Crear descuento
    db_descuento = Descuentos(
        Nombre=descuento.nombre,
        Descripcion=descuento.descripcion,
        Tipo_Descuento=descuento.tipo_descuento,
        Porcentaje=descuento.porcentaje if descuento.tipo_descuento == "Porcentaje" else None,
        Monto_Fijo=descuento.monto_fijo if descuento.tipo_descuento == "Monto Fijo" else None,
        Fecha_Inicio=descuento.fecha_inicio,
        Fecha_Fin=descuento.fecha_fin,
        Cantidad_Minima=descuento.cantidad_minima,
        Cantidad_Maxima=descuento.cantidad_maxima
    )
    db.add(db_descuento)
    db.flush()
    
    # Asociar productos
    if descuento.productos:
        for producto in descuento.productos:
            db_producto_descuento = Productos_Descuentos(
                ID_Producto=producto.id_producto,
                ID_Descuento=db_descuento.ID_Descuento
            )
            db.add(db_producto_descuento)
    
    db.commit()
    db.refresh(db_descuento)
    
    return await get_descuento(db_descuento.ID_Descuento, db, current_user)

# Actualizar descuento
@router.put("/{descuento_id}", response_model=DescuentoCompleto)
async def update_descuento(
    descuento: DescuentoUpdate,
    descuento_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_descuento = db.query(Descuentos).filter(Descuentos.ID_Descuento == descuento_id).first()
    if not db_descuento:
        raise HTTPException(status_code=404, detail="Descuento no encontrado")
    
    # Validaciones
    if descuento.fecha_inicio and descuento.fecha_fin:
        if descuento.fecha_inicio >= descuento.fecha_fin:
            raise HTTPException(
                status_code=400,
                detail="La fecha de fin debe ser posterior a la fecha de inicio"
            )
    elif descuento.fecha_inicio and descuento.fecha_inicio >= db_descuento.Fecha_Fin:
        raise HTTPException(
            status_code=400,
            detail="La fecha de inicio debe ser anterior a la fecha de fin actual"
        )
    elif descuento.fecha_fin and descuento.fecha_fin <= db_descuento.Fecha_Inicio:
        raise HTTPException(
            status_code=400,
            detail="La fecha de fin debe ser posterior a la fecha de inicio actual"
        )
    
    if descuento.tipo_descuento == "Porcentaje":
        if descuento.porcentaje and not 0 < descuento.porcentaje <= 100:
            raise HTTPException(
                status_code=400,
                detail="El porcentaje debe estar entre 0 y 100"
            )
    elif descuento.tipo_descuento == "Monto Fijo":
        if descuento.monto_fijo and descuento.monto_fijo <= 0:
            raise HTTPException(
                status_code=400,
                detail="El monto fijo debe ser mayor a 0"
            )
    
    # Actualizar campos
    for key, value in descuento.dict(exclude_unset=True).items():
        if key != "productos":
            setattr(db_descuento, key.capitalize(), value)
    
    # Actualizar productos si se proporcionan
    if descuento.productos is not None:
        # Eliminar asociaciones existentes
        db.query(Productos_Descuentos).filter(
            Productos_Descuentos.ID_Descuento == descuento_id
        ).delete()
        
        # Crear nuevas asociaciones
        for producto in descuento.productos:
            db_producto_descuento = Productos_Descuentos(
                ID_Producto=producto.id_producto,
                ID_Descuento=descuento_id
            )
            db.add(db_producto_descuento)
    
    db.commit()
    db.refresh(db_descuento)
    
    return await get_descuento(descuento_id, db, current_user)

# Obtener estadísticas de descuentos
@router.get("/estadisticas", response_model=EstadisticasDescuentos)
async def get_estadisticas_descuentos(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Filtro de fechas
    if not desde:
        desde = datetime.now() - timedelta(days=30)
    if not hasta:
        hasta = datetime.now()
    
    # Descuentos por tipo
    por_tipo = db.query(
        Descuentos.Tipo_Descuento,
        func.count(Descuentos.ID_Descuento).label('total'),
        func.avg(case(
            (Descuentos.Tipo_Descuento == 'Porcentaje', Descuentos.Porcentaje),
            else_=None
        )).label('promedio_porcentaje'),
        func.avg(case(
            (Descuentos.Tipo_Descuento == 'Monto Fijo', Descuentos.Monto_Fijo),
            else_=None
        )).label('promedio_monto')
    ).group_by(
        Descuentos.Tipo_Descuento
    ).all()
    
    # Productos más vendidos con descuento
    productos_descuento = db.query(
        Productos.ID_Producto,
        Productos.Nombre,
        func.count(Detalles_Factura_Venta.ID_Detalle).label('ventas'),
        func.sum(Detalles_Factura_Venta.Cantidad).label('unidades'),
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
    ).join(
        Productos_Descuentos,
        Productos_Descuentos.ID_Producto == Productos.ID_Producto
    ).join(
        Detalles_Factura_Venta,
        Detalles_Factura_Venta.ID_Producto == Productos.ID_Producto
    ).join(
        Facturas_Venta,
        and_(
            Facturas_Venta.ID_Factura_Venta == Detalles_Factura_Venta.ID_Factura_Venta,
            Facturas_Venta.Estado != 'Anulada',
            Facturas_Venta.Fecha.between(desde, hasta)
        )
    ).group_by(
        Productos.ID_Producto,
        Productos.Nombre
    ).order_by(
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).desc()
    ).limit(10).all()
    
    # Descuentos activos por fecha
    descuentos_activos = db.query(
        func.date(Facturas_Venta.Fecha).label('fecha'),
        func.count(distinct(Descuentos.ID_Descuento)).label('descuentos_activos'),
        func.sum(Detalles_Factura_Venta.Descuento_Unitario * Detalles_Factura_Venta.Cantidad).label('total_descuento')
    ).join(
        Productos_Descuentos,
        Productos_Descuentos.ID_Producto == Detalles_Factura_Venta.ID_Producto
    ).join(
        Descuentos,
        Descuentos.ID_Descuento == Productos_Descuentos.ID_Descuento
    ).filter(
        Facturas_Venta.Fecha.between(desde, hasta),
        Facturas_Venta.Estado != 'Anulada'
    ).group_by(
        func.date(Facturas_Venta.Fecha)
    ).order_by(
        func.date(Facturas_Venta.Fecha)
    ).all()
    
    return {
        "por_tipo": [
            {
                "tipo": t.Tipo_Descuento,
                "total": t.total,
                "promedio": round(t.promedio_porcentaje or t.promedio_monto or 0, 2)
            }
            for t in por_tipo
        ],
        "productos_destacados": [
            {
                "producto": {
                    "id": p.ID_Producto,
                    "nombre": p.Nombre
                },
                "ventas": p.ventas,
                "unidades": p.unidades,
                "total_descuento": p.total_descuento
            }
            for p in productos_descuento
        ],
        "evolucion_diaria": [
            {
                "fecha": d.fecha,
                "descuentos_activos": d.descuentos_activos,
                "total_descuento": d.total_descuento
            }
            for d in descuentos_activos
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
