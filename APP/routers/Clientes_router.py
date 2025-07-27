from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db
from ..schemas.Clientes_schema import (
    ClienteBase,
    ClienteCreate,
    ClienteUpdate,
    ClienteSimple,
    ClienteCompleta
)
from ..DB.Clientes_model import Clientes
from ..DB.Facturas_Venta_model import Facturas_Venta
from ..DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from ..routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)

# Obtener todos los clientes con paginación y filtros
@router.get("/", response_model=List[ClienteSimple])
async def get_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    activo: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    tipo_cliente: Optional[str] = Query(None, description="Filtrar por tipo de cliente"),
    provincia: Optional[str] = Query(None, description="Filtrar por provincia"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, CUIT/CUIL o email"),
    ordenar_por: Optional[str] = Query(None, description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(Clientes)
    
    # Aplicar filtros
    if activo is not None:
        query = query.filter(Clientes.Activo == activo)
    if tipo_cliente:
        query = query.filter(Clientes.Tipo_Cliente == tipo_cliente)
    if provincia:
        query = query.filter(Clientes.Provincia == provincia)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            (Clientes.Nombre.ilike(search)) |
            (Clientes.Apellido.ilike(search)) |
            (Clientes.CUIT_CUIL.ilike(search)) |
            (Clientes.Email.ilike(search))
        )
    
    # Aplicar ordenamiento
    if ordenar_por:
        orden_col = getattr(Clientes, ordenar_por.capitalize(), Clientes.Nombre)
        if orden == "desc":
            orden_col = orden_col.desc()
        query = query.order_by(orden_col)
    
    total = query.count()
    clientes = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": clientes,
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener un cliente por ID
@router.get("/{cliente_id}", response_model=ClienteCompleta)
async def get_cliente(
    cliente_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Crear nuevo cliente
@router.post("/", response_model=ClienteCompleta)
async def create_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar CUIT/CUIL único si se proporciona
    if cliente.cuit_cuil:
        existe_cuit = db.query(Clientes).filter(Clientes.CUIT_CUIL == cliente.cuit_cuil).first()
        if existe_cuit:
            raise HTTPException(status_code=400, detail="CUIT/CUIL ya registrado")
    
    # Verificar email único si se proporciona
    if cliente.email:
        existe_email = db.query(Clientes).filter(Clientes.Email == cliente.email).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Validar límite de crédito
    if cliente.limite_credito < 0:
        raise HTTPException(status_code=400, detail="El límite de crédito no puede ser negativo")
    
    # Crear cliente
    db_cliente = Clientes(
        Nombre=cliente.nombre,
        Apellido=cliente.apellido,
        CUIT_CUIL=cliente.cuit_cuil,
        Tipo_Cliente=cliente.tipo_cliente,
        Condicion_IVA=cliente.condicion_iva,
        Direccion=cliente.direccion,
        Localidad=cliente.localidad,
        Provincia=cliente.provincia,
        Codigo_Postal=cliente.codigo_postal,
        Telefono=cliente.telefono,
        Telefono_Alternativo=cliente.telefono_alternativo,
        Email=cliente.email,
        Fecha_Nacimiento=cliente.fecha_nacimiento,
        Genero=cliente.genero,
        Limite_Credito=cliente.limite_credito,
        Observaciones=cliente.observaciones
    )
    
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Actualizar cliente
@router.put("/{cliente_id}", response_model=ClienteCompleta)
async def update_cliente(
    cliente: ClienteUpdate,
    cliente_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    db_cliente = db.query(Clientes).filter(Clientes.ID_Cliente == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Verificar CUIT/CUIL único
    if cliente.cuit_cuil and cliente.cuit_cuil != db_cliente.CUIT_CUIL:
        existe_cuit = db.query(Clientes).filter(
            Clientes.CUIT_CUIL == cliente.cuit_cuil,
            Clientes.ID_Cliente != cliente_id
        ).first()
        if existe_cuit:
            raise HTTPException(status_code=400, detail="CUIT/CUIL ya registrado")
    
    # Verificar email único
    if cliente.email and cliente.email != db_cliente.Email:
        existe_email = db.query(Clientes).filter(
            Clientes.Email == cliente.email,
            Clientes.ID_Cliente != cliente_id
        ).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Validar límite de crédito
    if cliente.limite_credito is not None and cliente.limite_credito < 0:
        raise HTTPException(status_code=400, detail="El límite de crédito no puede ser negativo")
    
    # Actualizar campos
    for key, value in cliente.dict(exclude_unset=True).items():
        setattr(db_cliente, key.capitalize(), value)
    
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

# Obtener historial de compras
@router.get("/{cliente_id}/compras", response_model=List[dict])
async def get_historial_compras(
    cliente_id: int = Path(..., gt=0),
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Facturas_Venta.ID_Factura_Venta,
        Facturas_Venta.Numero_Factura,
        Facturas_Venta.Fecha,
        Facturas_Venta.Total,
        Facturas_Venta.Estado
    ).filter(Facturas_Venta.ID_Cliente == cliente_id)
    
    if desde:
        query = query.filter(Facturas_Venta.Fecha >= desde)
    if hasta:
        query = query.filter(Facturas_Venta.Fecha <= hasta)
    if estado:
        query = query.filter(Facturas_Venta.Estado == estado)
    
    compras = query.order_by(Facturas_Venta.Fecha.desc()).all()
    
    return [
        {
            "id": c.ID_Factura_Venta,
            "numero_factura": c.Numero_Factura,
            "fecha": c.Fecha,
            "total": c.Total,
            "estado": c.Estado
        }
        for c in compras
    ]

# Obtener estado de cuenta
@router.get("/{cliente_id}/estado-cuenta", response_model=dict)
async def get_estado_cuenta(
    cliente_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Facturas pendientes
    facturas_pendientes = db.query(
        func.count(Facturas_Venta.ID_Factura_Venta).label('cantidad'),
        func.sum(Facturas_Venta.Total).label('total')
    ).filter(
        Facturas_Venta.ID_Cliente == cliente_id,
        Facturas_Venta.Estado.in_(['Emitida', 'Pendiente'])
    ).first()
    
    # Últimas compras
    ultimas_compras = db.query(
        func.count(Facturas_Venta.ID_Factura_Venta).label('total'),
        func.sum(case((Facturas_Venta.Fecha >= datetime.now() - timedelta(days=30), 1), else_=0)).label('ultimo_mes'),
        func.sum(Facturas_Venta.Total).label('monto_total')
    ).filter(
        Facturas_Venta.ID_Cliente == cliente_id,
        Facturas_Venta.Estado != 'Anulada'
    ).first()
    
    return {
        "limite_credito": cliente.Limite_Credito,
        "saldo_actual": cliente.Saldo_Actual,
        "credito_disponible": cliente.Limite_Credito - cliente.Saldo_Actual,
        "facturas_pendientes": {
            "cantidad": facturas_pendientes.cantidad or 0,
            "total": facturas_pendientes.total or 0
        },
        "estadisticas_compras": {
            "total_compras": ultimas_compras.total or 0,
            "compras_ultimo_mes": ultimas_compras.ultimo_mes or 0,
            "monto_total": ultimas_compras.monto_total or 0
        }
    }

# Actualizar límite de crédito
@router.patch("/{cliente_id}/limite-credito")
async def update_limite_credito(
    cliente_id: int = Path(..., gt=0),
    nuevo_limite: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    if nuevo_limite < cliente.Saldo_Actual:
        raise HTTPException(
            status_code=400,
            detail="El nuevo límite no puede ser menor al saldo actual"
        )
    
    cliente.Limite_Credito = nuevo_limite
    db.commit()
    
    return {
        "message": "Límite de crédito actualizado",
        "nuevo_limite": nuevo_limite,
        "credito_disponible": nuevo_limite - cliente.Saldo_Actual
    }

# Obtener estadísticas de clientes
@router.get("/estadisticas/general", response_model=dict)
async def get_estadisticas_clientes(
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    total = db.query(func.count(Clientes.ID_Cliente)).scalar()
    activos = db.query(func.count(Clientes.ID_Cliente)).filter(Clientes.Activo == True).scalar()
    
    # Clientes por tipo
    por_tipo = db.query(
        Clientes.Tipo_Cliente,
        func.count(Clientes.ID_Cliente).label('total')
    ).group_by(Clientes.Tipo_Cliente).all()
    
    # Clientes por provincia
    por_provincia = db.query(
        Clientes.Provincia,
        func.count(Clientes.ID_Cliente).label('total')
    ).group_by(Clientes.Provincia).all()
    
    # Mejores clientes (por monto de compras)
    mejores_clientes = db.query(
        Clientes.ID_Cliente,
        Clientes.Nombre,
        Clientes.Apellido,
        func.count(Facturas_Venta.ID_Factura_Venta).label('total_compras'),
        func.sum(Facturas_Venta.Total).label('monto_total')
    ).join(Facturas_Venta).filter(
        Facturas_Venta.Estado != 'Anulada'
    ).group_by(
        Clientes.ID_Cliente,
        Clientes.Nombre,
        Clientes.Apellido
    ).order_by(func.sum(Facturas_Venta.Total).desc()).limit(5).all()
    
    return {
        "total_clientes": total,
        "clientes_activos": activos,
        "por_tipo": [
            {"tipo": t.Tipo_Cliente, "total": t.total}
            for t in por_tipo
        ],
        "por_provincia": [
            {"provincia": p.Provincia, "total": p.total}
            for p in por_provincia
        ],
        "mejores_clientes": [
            {
                "id": c.ID_Cliente,
                "nombre": f"{c.Nombre} {c.Apellido}",
                "total_compras": c.total_compras,
                "monto_total": c.monto_total
            }
            for c in mejores_clientes
        ]
    }
