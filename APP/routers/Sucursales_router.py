from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Sucursales_schema import (
    SucursalBase,
    SucursalCreate,
    SucursalUpdate,
    SucursalSimple,
    SucursalCompleta,
    SucursalList,
    SucursalEstadisticas
)
from APP.DB.Sucursales_model import Sucursales
from APP.DB.Usuarios_model import Usuarios
from APP.DB.Inventario_model import Inventario
from APP.DB.Facturas_Venta_model import Facturas_Venta
from sqlalchemy import func, and_, or_, distinct, case, exists
from datetime import datetime, time

router = APIRouter(
    prefix="/sucursales",
    tags=["Sucursales"]
)

# Obtener todas las sucursales con paginación y filtros
@router.get("/", response_model=SucursalList)
async def get_sucursales(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    provincia: Optional[str] = Query(None, description="Filtrar por provincia"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, dirección o localidad"),
    ordenar_por: Optional[str] = Query("nombre", description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db)
):
    # Query base con conteos
    query = db.query(
        Sucursales,
        func.count(distinct(Usuarios.ID_Usuario)).label('usuarios_count'),
        func.count(distinct(Inventario.ID_Inventario)).label('productos_count'),
        func.count(distinct(Facturas_Venta.ID_Factura_Venta)).label('ventas_count')
    ).outerjoin(
        Usuarios, and_(
            Usuarios.ID_Sucursal == Sucursales.ID_Sucursal,
            Usuarios.Estado == True
        )
    ).outerjoin(
        Inventario, and_(
            Inventario.ID_Sucursal == Sucursales.ID_Sucursal,
            Inventario.Activo == True
        )
    ).outerjoin(
        Facturas_Venta, and_(
            Facturas_Venta.ID_Sucursal == Sucursales.ID_Sucursal,
            Facturas_Venta.Estado != 'Anulada'
        )
    ).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Sucursales.Direccion,
        Sucursales.Telefono,
        Sucursales.Email,
        Sucursales.Localidad,
        Sucursales.Provincia,
        Sucursales.Codigo_Postal,
        Sucursales.Horario_Apertura,
        Sucursales.Horario_Cierre,
        Sucursales.Activo,
        Sucursales.Fecha_Creacion
    )
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Sucursales.Activo == activo)
    if provincia:
        query = query.filter(Sucursales.Provincia.ilike(f"%{provincia}%"))
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            or_(
                Sucursales.Nombre.ilike(search),
                Sucursales.Direccion.ilike(search),
                Sucursales.Localidad.ilike(search)
            )
        )
    
    # Contar total de registros
    total = db.query(func.count(Sucursales.ID_Sucursal)).scalar()
    
    # Aplicar ordenamiento (requerido por SQL Server para OFFSET/LIMIT)
    if ordenar_por == "nombre":
        if orden == "desc":
            query = query.order_by(Sucursales.Nombre.desc(), Sucursales.ID_Sucursal.asc())
        else:
            query = query.order_by(Sucursales.Nombre.asc(), Sucursales.ID_Sucursal.asc())
    elif ordenar_por == "localidad":
        if orden == "desc":
            query = query.order_by(Sucursales.Localidad.desc(), Sucursales.ID_Sucursal.asc())
        else:
            query = query.order_by(Sucursales.Localidad.asc(), Sucursales.ID_Sucursal.asc())
    elif ordenar_por == "provincia":
        if orden == "desc":
            query = query.order_by(Sucursales.Provincia.desc(), Sucursales.ID_Sucursal.asc())
        else:
            query = query.order_by(Sucursales.Provincia.asc(), Sucursales.ID_Sucursal.asc())
    else:
        # Ordenamiento por defecto
        query = query.order_by(Sucursales.ID_Sucursal.asc())
    
    # Aplicar paginación
    resultados = query.offset(skip).limit(limit).all()
    
    # Procesar resultados
    sucursales_procesadas = []
    for sucursal, usuarios_count, productos_count, ventas_count in resultados:
        sucursal_dict = {
            "id_sucursal": sucursal.ID_Sucursal,
            "nombre": sucursal.Nombre,
            "direccion": sucursal.Direccion,
            "telefono": sucursal.Telefono,
            "email": sucursal.Email,
            "localidad": sucursal.Localidad,
            "provincia": sucursal.Provincia,
            "codigo_postal": sucursal.Codigo_Postal,
            "horario_apertura": sucursal.Horario_Apertura.strftime("%H:%M") if sucursal.Horario_Apertura else None,
            "horario_cierre": sucursal.Horario_Cierre.strftime("%H:%M") if sucursal.Horario_Cierre else None,
            "activo": sucursal.Activo,
            "usuarios_count": usuarios_count,
            "productos_count": productos_count,
            "ventas_count": ventas_count
        }
        sucursales_procesadas.append(sucursal_dict)
    
    return {
        "total_registros": total,
        "pagina_actual": skip // limit + 1,
        "total_paginas": (total + limit - 1) // limit,
        "sucursales": sucursales_procesadas
    }

# Obtener estadísticas de sucursales
@router.get("/estadisticas", response_model=SucursalEstadisticas)
async def get_estadisticas_sucursales(
    db: Session = Depends(get_db)
):
    # Total de sucursales
    total_sucursales = db.query(func.count(Sucursales.ID_Sucursal)).scalar()
    
    # Sucursales activas
    sucursales_activas = db.query(func.count(Sucursales.ID_Sucursal)).filter(
        Sucursales.Activo == True
    ).scalar()
    
    # Sucursales por provincia
    sucursales_provincia = db.query(
        Sucursales.Provincia,
        func.count(Sucursales.ID_Sucursal).label('total_sucursales'),
        func.count(distinct(case([(Sucursales.Activo == True, Sucursales.ID_Sucursal)])))
            .label('sucursales_activas')
    ).group_by(
        Sucursales.Provincia
    ).order_by(
        func.count(Sucursales.ID_Sucursal).desc()
    ).all()
    
    # Sucursales con más ventas
    sucursales_ventas = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Sucursales.Localidad,
        Sucursales.Provincia,
        func.count(Facturas_Venta.ID_Factura_Venta).label('total_ventas'),
        func.sum(Facturas_Venta.Total).label('monto_total')
    ).outerjoin(
        Facturas_Venta, and_(
            Facturas_Venta.ID_Sucursal == Sucursales.ID_Sucursal,
            Facturas_Venta.Estado != 'Anulada'
        )
    ).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Sucursales.Localidad,
        Sucursales.Provincia
    ).order_by(
        func.count(Facturas_Venta.ID_Factura_Venta).desc()
    ).limit(5).all()
    
    return {
        "total_sucursales": total_sucursales,
        "sucursales_activas": sucursales_activas,
        "sucursales_por_provincia": [
            {
                "provincia": prov.Provincia,
                "total_sucursales": prov.total_sucursales,
                "sucursales_activas": prov.sucursales_activas
            }
            for prov in sucursales_provincia
        ],
        "sucursales_mas_ventas": [
            {
                "id": suc.ID_Sucursal,
                "nombre": suc.Nombre,
                "localidad": suc.Localidad,
                "provincia": suc.Provincia,
                "total_ventas": suc.total_ventas,
                "monto_total": float(suc.monto_total) if suc.monto_total else 0
            }
            for suc in sucursales_ventas
        ]
    }

# Obtener una sucursal por ID
@router.get("/{sucursal_id}", response_model=SucursalCompleta)
async def get_sucursal(
    sucursal_id: int = Path(..., gt=0, description="ID de la sucursal"),
    db: Session = Depends(get_db)
):
    # Query con conteos
    result = db.query(
        Sucursales,
        func.count(distinct(Usuarios.ID_Usuario)).label('usuarios_count'),
        func.count(distinct(Inventario.ID_Inventario)).label('productos_count'),
        func.count(distinct(Facturas_Venta.ID_Factura_Venta)).label('ventas_count')
    ).outerjoin(
        Usuarios, and_(
            Usuarios.ID_Sucursal == Sucursales.ID_Sucursal,
            Usuarios.Estado == True
        )
    ).outerjoin(
        Inventario, and_(
            Inventario.ID_Sucursal == Sucursales.ID_Sucursal,
            Inventario.Activo == True
        )
    ).outerjoin(
        Facturas_Venta, and_(
            Facturas_Venta.ID_Sucursal == Sucursales.ID_Sucursal,
            Facturas_Venta.Estado != 'Anulada'
        )
    ).filter(
        Sucursales.ID_Sucursal == sucursal_id
    ).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        Sucursales.Direccion,
        Sucursales.Telefono,
        Sucursales.Email,
        Sucursales.Localidad,
        Sucursales.Provincia,
        Sucursales.Codigo_Postal,
        Sucursales.Horario_Apertura,
        Sucursales.Horario_Cierre,
        Sucursales.Activo,
        Sucursales.Fecha_Creacion
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    sucursal, usuarios_count, productos_count, ventas_count = result
    
    return {
        "id_sucursal": sucursal.ID_Sucursal,
        "nombre": sucursal.Nombre,
        "direccion": sucursal.Direccion,
        "telefono": sucursal.Telefono,
        "email": sucursal.Email,
        "localidad": sucursal.Localidad,
        "provincia": sucursal.Provincia,
        "codigo_postal": sucursal.Codigo_Postal,
        "horario_apertura": sucursal.Horario_Apertura.strftime("%H:%M") if sucursal.Horario_Apertura else None,
        "horario_cierre": sucursal.Horario_Cierre.strftime("%H:%M") if sucursal.Horario_Cierre else None,
        "activo": sucursal.Activo,
        "fecha_creacion": sucursal.Fecha_Creacion,
        "usuarios_count": usuarios_count,
        "productos_count": productos_count,
        "ventas_count": ventas_count
    }

# Crear nueva sucursal
@router.post("/", response_model=SucursalCompleta)
async def create_sucursal(
    sucursal: SucursalCreate,
    db: Session = Depends(get_db)
):
    # Verificar si ya existe una sucursal con el mismo nombre
    existe = db.query(Sucursales).filter(Sucursales.Nombre == sucursal.nombre).first()
    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una sucursal con este nombre"
        )
    
    # Convertir horarios de string a time
    horario_apertura = datetime.strptime(sucursal.horario_apertura, "%H:%M").time() if sucursal.horario_apertura else None
    horario_cierre = datetime.strptime(sucursal.horario_cierre, "%H:%M").time() if sucursal.horario_cierre else None
    
    # Crear nueva sucursal
    db_sucursal = Sucursales(
        Nombre=sucursal.nombre,
        Direccion=sucursal.direccion,
        Telefono=sucursal.telefono,
        Email=sucursal.email,
        Localidad=sucursal.localidad,
        Provincia=sucursal.provincia,
        Codigo_Postal=sucursal.codigo_postal,
        Horario_Apertura=horario_apertura,
        Horario_Cierre=horario_cierre,
        Activo=sucursal.activo
    )
    db.add(db_sucursal)
    db.commit()
    db.refresh(db_sucursal)
    
    return {
        "id_sucursal": db_sucursal.ID_Sucursal,
        "nombre": db_sucursal.Nombre,
        "direccion": db_sucursal.Direccion,
        "telefono": db_sucursal.Telefono,
        "email": db_sucursal.Email,
        "localidad": db_sucursal.Localidad,
        "provincia": db_sucursal.Provincia,
        "codigo_postal": db_sucursal.Codigo_Postal,
        "horario_apertura": db_sucursal.Horario_Apertura.strftime("%H:%M") if db_sucursal.Horario_Apertura else None,
        "horario_cierre": db_sucursal.Horario_Cierre.strftime("%H:%M") if db_sucursal.Horario_Cierre else None,
        "activo": db_sucursal.Activo,
        "fecha_creacion": db_sucursal.Fecha_Creacion,
        "usuarios_count": 0,
        "productos_count": 0,
        "ventas_count": 0
    }

# Actualizar sucursal
@router.put("/{sucursal_id}", response_model=SucursalCompleta)
async def update_sucursal(
    sucursal: SucursalUpdate,
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar sucursal existente
    db_sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Verificar nombre único
    if sucursal.nombre:
        existe = db.query(Sucursales).filter(
            Sucursales.Nombre == sucursal.nombre,
            Sucursales.ID_Sucursal != sucursal_id
        ).first()
        if existe:
            raise HTTPException(
                status_code=400,
                detail="Ya existe una sucursal con este nombre"
            )
    
    # Actualizar campos
    update_data = sucursal.dict(exclude_unset=True)
    
    # Convertir horarios si están presentes
    if "horario_apertura" in update_data:
        update_data["Horario_Apertura"] = datetime.strptime(update_data.pop("horario_apertura"), "%H:%M").time() if update_data["horario_apertura"] else None
    if "horario_cierre" in update_data:
        update_data["Horario_Cierre"] = datetime.strptime(update_data.pop("horario_cierre"), "%H:%M").time() if update_data["horario_cierre"] else None
    
    # Actualizar campos con nombres capitalizados
    for key, value in update_data.items():
        setattr(db_sucursal, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_sucursal)
    
    # Obtener conteos actualizados
    conteos = db.query(
        func.count(distinct(Usuarios.ID_Usuario)).label('usuarios_count'),
        func.count(distinct(Inventario.ID_Inventario)).label('productos_count'),
        func.count(distinct(Facturas_Venta.ID_Factura_Venta)).label('ventas_count')
    ).select_from(Sucursales).outerjoin(
        Usuarios, and_(
            Usuarios.ID_Sucursal == sucursal_id,
            Usuarios.Estado == True
        )
    ).outerjoin(
        Inventario, and_(
            Inventario.ID_Sucursal == sucursal_id,
            Inventario.Activo == True
        )
    ).outerjoin(
        Facturas_Venta, and_(
            Facturas_Venta.ID_Sucursal == sucursal_id,
            Facturas_Venta.Estado != 'Anulada'
        )
    ).first()
    
    usuarios_count, productos_count, ventas_count = conteos
    
    return {
        "id_sucursal": db_sucursal.ID_Sucursal,
        "nombre": db_sucursal.Nombre,
        "direccion": db_sucursal.Direccion,
        "telefono": db_sucursal.Telefono,
        "email": db_sucursal.Email,
        "localidad": db_sucursal.Localidad,
        "provincia": db_sucursal.Provincia,
        "codigo_postal": db_sucursal.Codigo_Postal,
        "horario_apertura": db_sucursal.Horario_Apertura.strftime("%H:%M") if db_sucursal.Horario_Apertura else None,
        "horario_cierre": db_sucursal.Horario_Cierre.strftime("%H:%M") if db_sucursal.Horario_Cierre else None,
        "activo": db_sucursal.Activo,
        "fecha_creacion": db_sucursal.Fecha_Creacion,
        "usuarios_count": usuarios_count,
        "productos_count": productos_count,
        "ventas_count": ventas_count
    }

# Eliminar sucursal (soft delete)
@router.delete("/{sucursal_id}")
async def delete_sucursal(
    sucursal_id: int = Path(..., gt=0),
    db: Session = Depends(get_db)
):
    # Buscar sucursal
    db_sucursal = db.query(Sucursales).filter(
        Sucursales.ID_Sucursal == sucursal_id
    ).first()
    if not db_sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    # Verificar si tiene usuarios, inventario o ventas asociadas
    tiene_asociaciones = db.query(
        or_(
            exists().where(and_(Usuarios.ID_Sucursal == sucursal_id, Usuarios.Estado == True)),
            exists().where(and_(Inventario.ID_Sucursal == sucursal_id, Inventario.Activo == True)),
            exists().where(Facturas_Venta.ID_Sucursal == sucursal_id)
        )
    ).scalar()
    
    if tiene_asociaciones:
        # Soft delete
        db_sucursal.Activo = False
        db.commit()
        return {"message": "Sucursal desactivada porque tiene elementos asociados"}
    else:
        # Hard delete si no tiene asociaciones
        db.delete(db_sucursal)
        db.commit()
        return {"message": "Sucursal eliminada"}
