from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Auditoria_Cambios_schema import (
    AuditoriaCambiosBase,
    AuditoriaCambiosCreate,
    AuditoriaCambiosSimple,
    AuditoriaCambiosCompleta,
    EstadisticasAuditoria,
    BusquedaAuditoria
)
from APP.DB.Auditoria_Cambios_model import Auditoria_Cambios
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case, distinct, or_, cast, JSON
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user
import json

router = APIRouter(
    prefix="/auditoria",
    tags=["Auditoría de Cambios"]
)

# Obtener registros de auditoría con filtros
@router.get("/", response_model=List[AuditoriaCambiosSimple])
async def get_auditoria(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tabla: Optional[str] = Query(None, description="Filtrar por tabla afectada"),
    tipo_operacion: Optional[str] = Query(None, description="Filtrar por tipo de operación"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por usuario"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(
        Auditoria_Cambios,
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Usuarios
    )
    
    # Aplicar filtros
    if tabla:
        query = query.filter(Auditoria_Cambios.Tabla_Afectada == tabla)
    if tipo_operacion:
        query = query.filter(Auditoria_Cambios.Tipo_Operacion == tipo_operacion)
    if usuario_id:
        query = query.filter(Auditoria_Cambios.ID_Usuario == usuario_id)
    if desde:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion >= desde)
    if hasta:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion <= hasta)
    
    total = query.count()
    registros = query.order_by(Auditoria_Cambios.Fecha_Operacion.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_auditoria": r.Auditoria_Cambios.ID_Auditoria,
                "tabla": r.Auditoria_Cambios.Tabla_Afectada,
                "id_registro": r.Auditoria_Cambios.ID_Registro,
                "tipo_operacion": r.Auditoria_Cambios.Tipo_Operacion,
                "fecha": r.Auditoria_Cambios.Fecha_Operacion,
                "usuario": f"{r.nombre_usuario} {r.apellido_usuario}",
                "ip_cliente": r.Auditoria_Cambios.IP_Cliente
            }
            for r in registros
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Buscar cambios por registro
@router.get("/buscar", response_model=BusquedaAuditoria)
async def buscar_cambios(
    tabla: str = Query(..., description="Nombre de la tabla"),
    id_registro: int = Query(..., gt=0, description="ID del registro a buscar"),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(
        Auditoria_Cambios,
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Usuarios
    ).filter(
        Auditoria_Cambios.Tabla_Afectada == tabla,
        Auditoria_Cambios.ID_Registro == id_registro
    )
    
    if desde:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion >= desde)
    if hasta:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion <= hasta)
    
    cambios = query.order_by(Auditoria_Cambios.Fecha_Operacion).all()
    
    historial = []
    estado_actual = {}
    
    for cambio in cambios:
        try:
            datos_anteriores = json.loads(cambio.Auditoria_Cambios.Datos_Anteriores) if cambio.Auditoria_Cambios.Datos_Anteriores else {}
            datos_nuevos = json.loads(cambio.Auditoria_Cambios.Datos_Nuevos) if cambio.Auditoria_Cambios.Datos_Nuevos else {}
            
            # Actualizar estado actual
            if cambio.Auditoria_Cambios.Tipo_Operacion == "INSERT":
                estado_actual.update(datos_nuevos)
            elif cambio.Auditoria_Cambios.Tipo_Operacion == "UPDATE":
                estado_actual.update(datos_nuevos)
            elif cambio.Auditoria_Cambios.Tipo_Operacion == "DELETE":
                estado_actual = {}
            
            historial.append({
                "id_auditoria": cambio.Auditoria_Cambios.ID_Auditoria,
                "tipo_operacion": cambio.Auditoria_Cambios.Tipo_Operacion,
                "fecha": cambio.Auditoria_Cambios.Fecha_Operacion,
                "usuario": f"{cambio.nombre_usuario} {cambio.apellido_usuario}",
                "datos_anteriores": datos_anteriores,
                "datos_nuevos": datos_nuevos,
                "ip_cliente": cambio.Auditoria_Cambios.IP_Cliente
            })
        except json.JSONDecodeError:
            # Si no se puede parsear JSON, usar texto plano
            historial.append({
                "id_auditoria": cambio.Auditoria_Cambios.ID_Auditoria,
                "tipo_operacion": cambio.Auditoria_Cambios.Tipo_Operacion,
                "fecha": cambio.Auditoria_Cambios.Fecha_Operacion,
                "usuario": f"{cambio.nombre_usuario} {cambio.apellido_usuario}",
                "datos_anteriores": cambio.Auditoria_Cambios.Datos_Anteriores,
                "datos_nuevos": cambio.Auditoria_Cambios.Datos_Nuevos,
                "ip_cliente": cambio.Auditoria_Cambios.IP_Cliente
            })
    
    return {
        "tabla": tabla,
        "id_registro": id_registro,
        "estado_actual": estado_actual,
        "historial": historial,
        "total_cambios": len(historial)
    }

# Obtener estadísticas de auditoría
@router.get("/estadisticas", response_model=EstadisticasAuditoria)
async def get_estadisticas_auditoria(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(Auditoria_Cambios)
    
    if desde:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion >= desde)
    if hasta:
        query = query.filter(Auditoria_Cambios.Fecha_Operacion <= hasta)
    
    # Totales
    total_registros = query.count()
    
    # Por tipo de operación
    por_operacion = db.query(
        Auditoria_Cambios.Tipo_Operacion,
        func.count(Auditoria_Cambios.ID_Auditoria).label('cantidad')
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(Auditoria_Cambios.Tipo_Operacion).all()
    
    # Por tabla
    por_tabla = db.query(
        Auditoria_Cambios.Tabla_Afectada,
        func.count(Auditoria_Cambios.ID_Auditoria).label('cantidad')
    ).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(Auditoria_Cambios.Tabla_Afectada).order_by(
        func.count(Auditoria_Cambios.ID_Auditoria).desc()
    ).limit(10).all()
    
    # Por usuario
    por_usuario = db.query(
        Usuarios.Nombre,
        Usuarios.Apellido,
        func.count(Auditoria_Cambios.ID_Auditoria).label('cantidad')
    ).join(Auditoria_Cambios).filter(
        *query.whereclause.clauses if query.whereclause else []
    ).group_by(
        Usuarios.ID_Usuario,
        Usuarios.Nombre,
        Usuarios.Apellido
    ).order_by(
        func.count(Auditoria_Cambios.ID_Auditoria).desc()
    ).limit(10).all()
    
    # Actividad por día (últimos 30 días)
    actividad_diaria = db.query(
        func.date(Auditoria_Cambios.Fecha_Operacion).label('fecha'),
        func.count(Auditoria_Cambios.ID_Auditoria).label('cantidad')
    ).filter(
        Auditoria_Cambios.Fecha_Operacion >= datetime.now() - timedelta(days=30)
    ).group_by(
        func.date(Auditoria_Cambios.Fecha_Operacion)
    ).order_by(
        func.date(Auditoria_Cambios.Fecha_Operacion).desc()
    ).all()
    
    return {
        "total_registros": total_registros,
        "por_operacion": [
            {
                "tipo": p.Tipo_Operacion,
                "cantidad": p.cantidad
            }
            for p in por_operacion
        ],
        "por_tabla": [
            {
                "tabla": p.Tabla_Afectada,
                "cantidad": p.cantidad
            }
            for p in por_tabla
        ],
        "por_usuario": [
            {
                "usuario": f"{p.Nombre} {p.Apellido}",
                "cantidad": p.cantidad
            }
            for p in por_usuario
        ],
        "actividad_diaria": [
            {
                "fecha": p.fecha,
                "cantidad": p.cantidad
            }
            for p in actividad_diaria
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }

# Obtener un registro específico de auditoría
@router.get("/{auditoria_id}", response_model=AuditoriaCambiosCompleta)
async def get_registro_auditoria(
    auditoria_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    registro = db.query(
        Auditoria_Cambios,
        Usuarios.Nombre.label('nombre_usuario'),
        Usuarios.Apellido.label('apellido_usuario')
    ).join(
        Usuarios
    ).filter(
        Auditoria_Cambios.ID_Auditoria == auditoria_id
    ).first()
    
    if not registro:
        raise HTTPException(status_code=404, detail="Registro de auditoría no encontrado")
    
    # Procesar datos anteriores y nuevos
    try:
        datos_anteriores = json.loads(registro.Auditoria_Cambios.Datos_Anteriores) if registro.Auditoria_Cambios.Datos_Anteriores else None
        datos_nuevos = json.loads(registro.Auditoria_Cambios.Datos_Nuevos) if registro.Auditoria_Cambios.Datos_Nuevos else None
        
        # Calcular diferencias si ambos datos existen
        diferencias = []
        if datos_anteriores and datos_nuevos:
            for key in set(datos_anteriores.keys()) | set(datos_nuevos.keys()):
                valor_anterior = datos_anteriores.get(key)
                valor_nuevo = datos_nuevos.get(key)
                if valor_anterior != valor_nuevo:
                    diferencias.append({
                        "campo": key,
                        "anterior": valor_anterior,
                        "nuevo": valor_nuevo
                    })
    except json.JSONDecodeError:
        datos_anteriores = registro.Auditoria_Cambios.Datos_Anteriores
        datos_nuevos = registro.Auditoria_Cambios.Datos_Nuevos
        diferencias = None
    
    return {
        "registro": {
            "id_auditoria": registro.Auditoria_Cambios.ID_Auditoria,
            "tabla": registro.Auditoria_Cambios.Tabla_Afectada,
            "id_registro": registro.Auditoria_Cambios.ID_Registro,
            "tipo_operacion": registro.Auditoria_Cambios.Tipo_Operacion,
            "fecha": registro.Auditoria_Cambios.Fecha_Operacion,
            "usuario": {
                "id": registro.Auditoria_Cambios.ID_Usuario,
                "nombre": f"{registro.nombre_usuario} {registro.apellido_usuario}"
            },
            "ip_cliente": registro.Auditoria_Cambios.IP_Cliente
        },
        "datos": {
            "anteriores": datos_anteriores,
            "nuevos": datos_nuevos,
            "diferencias": diferencias
        }
    }


        Auditoria_Cambios.Fecha_Operacion.between(desde, hasta)
    ).group_by(
        Auditoria_Cambios.Tabla_Afectada
    ).all()
    
    # Cambios por tipo de operación
    por_operacion = db.query(
        Auditoria_Cambios.Tipo_Operacion,
        func.count(Auditoria_Cambios.ID_Auditoria).label('total'),
        func.count(distinct(Auditoria_Cambios.Tabla_Afectada)).label('tablas_afectadas')
    ).filter(
        Auditoria_Cambios.Fecha_Operacion.between(desde, hasta)
    ).group_by(
        Auditoria_Cambios.Tipo_Operacion
    ).all()
    
    # Usuarios más activos
    usuarios_activos = db.query(
        Usuarios.ID_Usuario,
        Usuarios.Nombre,
        Usuarios.Apellido,
        Usuarios.Rol,
        func.count(Auditoria_Cambios.ID_Auditoria).label('total_cambios'),
        func.count(distinct(Auditoria_Cambios.Tabla_Afectada)).label('tablas_diferentes')
    ).join(
        Auditoria_Cambios
    ).filter(
        Auditoria_Cambios.Fecha_Operacion.between(desde, hasta)
    ).group_by(
        Usuarios.ID_Usuario,
        Usuarios.Nombre,
        Usuarios.Apellido,
        Usuarios.Rol
    ).order_by(
        func.count(Auditoria_Cambios.ID_Auditoria).desc()
    ).limit(10).all()
    
    # Actividad por hora del día
    por_hora = db.query(
        func.extract('hour', Auditoria_Cambios.Fecha_Operacion).label('hora'),
        func.count(Auditoria_Cambios.ID_Auditoria).label('total')
    ).filter(
        Auditoria_Cambios.Fecha_Operacion.between(desde, hasta)
    ).group_by(
        func.extract('hour', Auditoria_Cambios.Fecha_Operacion)
    ).order_by(
        'hora'
    ).all()
    
    return {
        "por_tabla": [
            {
                "tabla": t.Tabla_Afectada,
                "total_cambios": t.total_cambios,
                "registros_afectados": t.registros_afectados,
                "usuarios_distintos": t.usuarios_distintos
            }
            for t in por_tabla
        ],
        "por_operacion": [
            {
                "tipo": o.Tipo_Operacion,
                "total": o.total,
                "tablas_afectadas": o.tablas_afectadas
            }
            for o in por_operacion
        ],
        "usuarios_activos": [
            {
                "usuario": {
                    "id": u.ID_Usuario,
                    "nombre": f"{u.Nombre} {u.Apellido}",
                    "rol": u.Rol
                },
                "total_cambios": u.total_cambios,
                "tablas_diferentes": u.tablas_diferentes
            }
            for u in usuarios_activos
        ],
        "actividad_horaria": [
            {
                "hora": h.hora,
                "total": h.total
            }
            for h in por_hora
        ],
        "periodo": {
            "desde": desde,
            "hasta": hasta
        }
    }
