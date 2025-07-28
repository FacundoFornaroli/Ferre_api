from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Ordenes_Compra_schema import (
    OrdenCompraBase,
    OrdenCompraCreate,
    OrdenCompraUpdate,
    OrdenCompraSimple,
    OrdenCompraCompleta,
    DetalleOCCreate
)
from APP.DB.Ordenes_Compra_model import Ordenes_Compra
from APP.DB.Detalle_OC_model import Detalle_OC
from APP.DB.Proveedores_model import Proveedores
from APP.DB.Productos_model import Productos
from APP.DB.Sucursales_model import Sucursales
from APP.DB.Usuarios_model import Usuarios
from APP.DB.Inventario_model import Inventario
from APP.DB.Movimientos_inventario_model import Movimientos_inventario
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/ordenes-compra",
    tags=["Órdenes de Compra"]
)

# Obtener todas las órdenes con paginación y filtros
@router.get("/", response_model=List[OrdenCompraSimple])
async def get_ordenes_compra(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    proveedor_id: Optional[int] = Query(None, description="Filtrar por proveedor"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    estado: Optional[str] = Query(None, description="Filtrar por estado"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Ordenes_Compra,
        Proveedores.Nombre.label('nombre_proveedor'),
        Sucursales.Nombre.label('nombre_sucursal')
    ).join(
        Proveedores
    ).join(
        Sucursales
    )
    
    # Aplicar filtros
    if proveedor_id:
        query = query.filter(Ordenes_Compra.ID_Proveedor == proveedor_id)
    if sucursal_id:
        query = query.filter(Ordenes_Compra.ID_Sucursal == sucursal_id)
    if estado:
        query = query.filter(Ordenes_Compra.Estado == estado)
    if desde:
        query = query.filter(Ordenes_Compra.Fecha >= desde)
    if hasta:
        query = query.filter(Ordenes_Compra.Fecha <= hasta)
    
    total = query.count()
    ordenes = query.order_by(Ordenes_Compra.Fecha.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_oc": o.Ordenes_Compra.ID_OC,
                "numero_oc": o.Ordenes_Compra.Numero_OC,
                "proveedor": {
                    "id": o.Ordenes_Compra.ID_Proveedor,
                    "nombre": o.nombre_proveedor
                },
                "sucursal": {
                    "id": o.Ordenes_Compra.ID_Sucursal,
                    "nombre": o.nombre_sucursal
                },
                "fecha": o.Ordenes_Compra.Fecha,
                "fecha_entrega_esperada": o.Ordenes_Compra.Fecha_Entrega_Esperada,
                "total": o.Ordenes_Compra.Total,
                "estado": o.Ordenes_Compra.Estado
            }
            for o in ordenes
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener una orden específica con sus detalles
@router.get("/{orden_id}", response_model=OrdenCompraCompleta)
async def get_orden_compra(
    orden_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    orden = db.query(
        Ordenes_Compra,
        Proveedores.Nombre.label('nombre_proveedor'),
        Sucursales.Nombre.label('nombre_sucursal'),
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Proveedores
    ).join(
        Sucursales
    ).join(
        Usuarios
    ).filter(
        Ordenes_Compra.ID_OC == orden_id
    ).first()
    
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    detalles = db.query(
        Detalle_OC,
        Productos.Nombre.label('nombre_producto'),
        Productos.Codigo_Barras,
        Productos.SKU
    ).join(
        Productos
    ).filter(
        Detalle_OC.ID_OC == orden_id
    ).all()
    
    return {
        "orden": {
            "id_oc": orden.Ordenes_Compra.ID_OC,
            "numero_oc": orden.Ordenes_Compra.Numero_OC,
            "proveedor": {
                "id": orden.Ordenes_Compra.ID_Proveedor,
                "nombre": orden.nombre_proveedor
            },
            "sucursal": {
                "id": orden.Ordenes_Compra.ID_Sucursal,
                "nombre": orden.nombre_sucursal
            },
            "usuario": {
                "id": orden.Ordenes_Compra.ID_Usuario,
                "nombre": f"{orden.nombre_usuario} {orden.apellido_usuario}"
            },
            "fecha": orden.Ordenes_Compra.Fecha,
            "fecha_entrega_esperada": orden.Ordenes_Compra.Fecha_Entrega_Esperada,
            "subtotal": orden.Ordenes_Compra.Subtotal,
            "iva": orden.Ordenes_Compra.IVA,
            "descuento": orden.Ordenes_Compra.Descuento,
            "total": orden.Ordenes_Compra.Total,
            "estado": orden.Ordenes_Compra.Estado,
            "observaciones": orden.Ordenes_Compra.Observaciones
        },
        "detalles": [
            {
                "id_detalle": d.Detalle_OC.ID_Detalle_OC,
                "producto": {
                    "id": d.Detalle_OC.ID_Producto,
                    "nombre": d.nombre_producto,
                    "codigo_barras": d.Codigo_Barras,
                    "sku": d.SKU
                },
                "cantidad": d.Detalle_OC.Cantidad,
                "costo_unitario": d.Detalle_OC.Costo_Unitario,
                "descuento_unitario": d.Detalle_OC.Descuento_Unitario,
                "subtotal": d.Detalle_OC.Subtotal
            }
            for d in detalles
        ]
    }

# Crear nueva orden de compra
@router.post("/", response_model=OrdenCompraCompleta)
async def create_orden_compra(
    orden: OrdenCompraCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar proveedor
    proveedor = db.query(Proveedores).filter(
        Proveedores.ID_Proveedor == orden.id_proveedor,
        Proveedores.Activo == True
    ).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado o inactivo")
    
    # Verificar sucursal
    sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == orden.id_sucursal,
        Sucursales.Activo == True
    ).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada o inactiva")
    
    # Verificar productos y calcular totales
    subtotal = 0
    detalles_db = []
    
    for detalle in orden.detalles:
        producto = db.query(Productos).filter(
            Productos.ID_Producto == detalle.id_producto,
            Productos.Activo == True
        ).first()
        if not producto:
            raise HTTPException(
                status_code=404,
                detail=f"Producto {detalle.id_producto} no encontrado o inactivo"
            )
        
        # Calcular subtotal del detalle
        subtotal_detalle = (detalle.cantidad * detalle.costo_unitario) - (detalle.cantidad * detalle.descuento_unitario)
        subtotal += subtotal_detalle
        
        detalles_db.append(
            Detalle_OC(
                ID_Producto=detalle.id_producto,
                Cantidad=detalle.cantidad,
                Costo_Unitario=detalle.costo_unitario,
                Descuento_Unitario=detalle.descuento_unitario,
                Subtotal=subtotal_detalle
            )
        )
    
    # Calcular totales
    iva = subtotal * 0.21  # 21% de IVA
    total = subtotal + iva - orden.descuento
    
    # Crear orden
    db_orden = Ordenes_Compra(
        ID_Proveedor=orden.id_proveedor,
        ID_Sucursal=orden.id_sucursal,
        Fecha_Entrega_Esperada=orden.fecha_entrega_esperada,
        Subtotal=subtotal,
        IVA=iva,
        Descuento=orden.descuento,
        Total=total,
        ID_Usuario=current_user.ID_Usuario,
        Observaciones=orden.observaciones
    )
    
    db.add(db_orden)
    db.flush()  # Para obtener el ID_OC
    
    # Asignar orden a los detalles y guardar
    for detalle in detalles_db:
        detalle.ID_OC = db_orden.ID_OC
        db.add(detalle)
    
    db.commit()
    db.refresh(db_orden)
    
    # Retornar la orden completa
    return await get_orden_compra(db_orden.ID_OC, db, current_user)

# Actualizar estado de orden de compra
@router.patch("/{orden_id}/estado")
async def update_estado_orden(
    orden_id: int = Path(..., gt=0),
    estado: str = Query(..., description="Nuevo estado de la orden"),
    observaciones: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    orden = db.query(Ordenes_Compra).filter(Ordenes_Compra.ID_OC == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    
    estados_validos = {
        "Pendiente": ["Aprobada", "Cancelada"],
        "Aprobada": ["Recibida", "Cancelada"],
        "Recibida": [],
        "Cancelada": []
    }
    
    if estado not in estados_validos.get(orden.Estado, []):
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar el estado de {orden.Estado} a {estado}"
        )
    
    # Si se recibe la orden, actualizar inventario
    if estado == "Recibida":
        detalles = db.query(Detalle_OC).filter(Detalle_OC.ID_OC == orden_id).all()
        
        for detalle in detalles:
            # Actualizar o crear registro de inventario
            inventario = db.query(Inventario).filter(
                Inventario.ID_Producto == detalle.ID_Producto,
                Inventario.ID_Sucursal == orden.ID_Sucursal
            ).first()
            
            if not inventario:
                inventario = Inventario(
                    ID_Producto=detalle.ID_Producto,
                    ID_Sucursal=orden.ID_Sucursal,
                    Stock_Actual=0,
                    Stock_Minimo=0,
                    Stock_Maximo=999999
                )
                db.add(inventario)
                db.flush()
            
            # Actualizar stock
            inventario.Stock_Actual += detalle.Cantidad
            inventario.Fecha_Ultimo_Movimiento = datetime.now()
            
            # Registrar movimiento
            movimiento = Movimientos_inventario(
                ID_Producto=detalle.ID_Producto,
                ID_Sucursal=orden.ID_Sucursal,
                Tipo="Compra",
                Cantidad=detalle.Cantidad,
                Costo_Unitario=detalle.Costo_Unitario,
                ID_Usuario=current_user.ID_Usuario,
                ID_Referencia=orden_id,
                Tipo_Referencia="OC"
            )
            db.add(movimiento)
    
    # Actualizar estado
    orden.Estado = estado
    if observaciones:
        orden.Observaciones = (orden.Observaciones or "") + f"\n[{datetime.now()}] {estado}: {observaciones}"
    
    db.commit()
    
    return {"message": f"Estado actualizado a {estado}"}

# Obtener estadísticas de órdenes de compra
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_oc(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(Ordenes_Compra)
    
    if desde:
        query = query.filter(Ordenes_Compra.Fecha >= desde)
    if hasta:
        query = query.filter(Ordenes_Compra.Fecha <= hasta)
    
    # Totales por estado
    por_estado = db.query(
        Ordenes_Compra.Estado,
        func.count(Ordenes_Compra.ID_OC).label('cantidad'),
        func.sum(Ordenes_Compra.Total).label('total')
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(Ordenes_Compra.Estado).all()
    
    # Totales por proveedor
    por_proveedor = db.query(
        Proveedores.ID_Proveedor,
        Proveedores.Nombre,
        func.count(Ordenes_Compra.ID_OC).label('cantidad'),
        func.sum(Ordenes_Compra.Total).label('total')
    ).join(
        Ordenes_Compra
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(
        Proveedores.ID_Proveedor,
        Proveedores.Nombre
    ).order_by(
        func.sum(Ordenes_Compra.Total).desc()
    ).limit(10).all()
    
    # Tiempo promedio de entrega
    tiempo_entrega = db.query(
        func.avg(
            func.datediff(
                'day',
                Ordenes_Compra.Fecha,
                Ordenes_Compra.Fecha_Entrega_Esperada
            )
        ).label('promedio_dias')
    ).filter(
        Ordenes_Compra.Estado == 'Recibida',
        *query.whereclause.clauses if query.whereclause else []
    ).scalar()
    
    return {
        "por_estado": [
            {
                "estado": p.Estado,
                "cantidad": p.cantidad,
                "total": p.total
            }
            for p in por_estado
        ],
        "por_proveedor": [
            {
                "proveedor": {
                    "id": p.ID_Proveedor,
                    "nombre": p.Nombre
                },
                "cantidad": p.cantidad,
                "total": p.total
            }
            for p in por_proveedor
        ],
        "tiempo_entrega": {
            "promedio_dias": round(tiempo_entrega, 1) if tiempo_entrega else 0
        },
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
