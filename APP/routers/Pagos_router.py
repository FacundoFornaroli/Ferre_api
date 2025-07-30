from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from APP.schemas.Pagos_schema import (
    PagoBase,
    PagoCreate,
    PagoUpdate,
    PagoSimple,
    PagoCompleto
)
from APP.DB.Pagos_model import Pagos
from APP.DB.Facturas_Venta_model import Facturas_Venta
from APP.DB.Clientes_model import Clientes
from APP.DB.Usuarios_model import Usuarios
from sqlalchemy import func, and_, case
from datetime import datetime, timedelta
from APP.routers.Usuarios_router import get_current_user

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)

# Obtener todos los pagos con paginación y filtros
@router.get("/", response_model=List[PagoSimple])
async def get_pagos(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    factura_id: Optional[int] = Query(None, description="Filtrar por factura"),
    metodo: Optional[str] = Query(None, description="Filtrar por método de pago"),
    desde: Optional[datetime] = Query(None, description="Fecha inicial"),
    hasta: Optional[datetime] = Query(None, description="Fecha final"),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    query = db.query(
        Pagos,
        Facturas_Venta.Numero_Factura,
        Clientes.Nombre.label('nombre_cliente'),
        Clientes.Apellido.label('apellido_cliente')
    ).join(
        Facturas_Venta
    ).join(
        Clientes,
        Facturas_Venta.ID_Cliente == Clientes.ID_Cliente
    )
    
    # Aplicar filtros
    if factura_id:
        query = query.filter(Pagos.ID_Factura_Venta == factura_id)
    if metodo:
        query = query.filter(Pagos.Metodo == metodo)
    if desde:
        query = query.filter(Pagos.Fecha >= desde)
    if hasta:
        query = query.filter(Pagos.Fecha <= hasta)
    
    total = query.count()
    pagos = query.order_by(Pagos.Fecha.desc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "items": [
            {
                "id_pago": p.Pagos.ID_Pago,
                "factura": {
                    "id": p.Pagos.ID_Factura_Venta,
                    "numero": p.Numero_Factura
                },
                "cliente": f"{p.nombre_cliente} {p.apellido_cliente}",
                "metodo": p.Pagos.Metodo,
                "monto": p.Pagos.Monto,
                "fecha": p.Pagos.Fecha
            }
            for p in pagos
        ],
        "pagina": skip // limit + 1,
        "paginas": (total + limit - 1) // limit
    }

# Obtener pagos por factura
@router.get("/factura/{factura_id}", response_model=List[PagoCompleto])
async def get_pagos_factura(
    factura_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar factura
    factura = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Factura_Venta == factura_id
    ).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    # Obtener pagos
    pagos = db.query(Pagos).filter(
        Pagos.ID_Factura_Venta == factura_id
    ).order_by(Pagos.Fecha.desc()).all()
    
    return pagos

# Obtener estadísticas de pagos
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_pagos(
    desde: Optional[datetime] = None,
    hasta: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol.lower() not in ["admin", "supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    query = db.query(Pagos)
    
    if desde:
        query = query.filter(Pagos.Fecha >= desde)
    if hasta:
        query = query.filter(Pagos.Fecha <= hasta)
    
    # Total de pagos
    total_pagos = query.count()
    total_monto = query.with_entities(func.sum(Pagos.Monto)).scalar() or 0
    
    # Por método de pago
    por_metodo = db.query(
        Pagos.Metodo,
        func.count(Pagos.ID_Pago).label('cantidad'),
        func.sum(Pagos.Monto).label('total')
    ).group_by(Pagos.Metodo).all()
    
    # Promedio por pago
    promedio_pago = total_monto / total_pagos if total_pagos > 0 else 0
    
    # Últimos 7 días
    ultimos_7_dias = db.query(
        func.count(Pagos.ID_Pago).label('cantidad'),
        func.sum(Pagos.Monto).label('total')
    ).filter(
        Pagos.Fecha >= datetime.now() - timedelta(days=7)
    ).first()
    
    return {
        "total_pagos": total_pagos,
        "total_monto": float(total_monto),
        "promedio_pago": float(promedio_pago),
        "por_metodo": [
            {
                "metodo": p.Metodo,
                "cantidad": p.cantidad,
                "total": float(p.total)
            }
            for p in por_metodo
        ],
        "ultimos_7_dias": {
            "cantidad": ultimos_7_dias.cantidad or 0,
            "total": float(ultimos_7_dias.total or 0)
        }
    }

# Obtener resumen de pagos por cliente
@router.get("/cliente/{cliente_id}/resumen", response_model=dict)
async def get_resumen_cliente(
    cliente_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar cliente
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # Obtener facturas del cliente
    facturas = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Cliente == cliente_id
    ).all()
    
    factura_ids = [f.ID_Factura_Venta for f in facturas]
    
    # Obtener pagos
    pagos = db.query(Pagos).filter(
        Pagos.ID_Factura_Venta.in_(factura_ids)
    ).all()
    
    total_pagado = sum(p.Monto for p in pagos)
    total_facturado = sum(f.Total for f in facturas)
    saldo_pendiente = total_facturado - total_pagado
    
    return {
        "cliente": {
            "id": cliente.ID_Cliente,
            "nombre": f"{cliente.Nombre} {cliente.Apellido}",
            "cuit": cliente.CUIT_CUIL
        },
        "resumen": {
            "total_facturado": float(total_facturado),
            "total_pagado": float(total_pagado),
            "saldo_pendiente": float(saldo_pendiente),
            "cantidad_facturas": len(facturas),
            "cantidad_pagos": len(pagos)
        },
        "ultimo_pago": {
            "fecha": max(p.Fecha for p in pagos) if pagos else None,
            "monto": float(max(p.Monto for p in pagos)) if pagos else 0
        }
    }

# Obtener un pago específico
@router.get("/{pago_id}", response_model=PagoCompleto)
async def get_pago(
    pago_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    pago = db.query(Pagos).filter(Pagos.ID_Pago == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

# Registrar nuevo pago
@router.post("/", response_model=PagoCompleto)
async def create_pago(
    pago: PagoCreate,
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    # Verificar factura
    factura = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Factura_Venta == pago.id_factura_venta
    ).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    if factura.Estado == "Anulada":
        raise HTTPException(status_code=400, detail="No se pueden registrar pagos en facturas anuladas")
    
    if factura.Estado == "Pagada":
        raise HTTPException(status_code=400, detail="La factura ya está pagada")
    
    # Verificar que el monto no exceda el saldo pendiente
    pagos_anteriores = db.query(func.sum(Pagos.Monto)).filter(
        Pagos.ID_Factura_Venta == pago.id_factura_venta
    ).scalar() or 0
    
    saldo_pendiente = factura.Total - pagos_anteriores
    if pago.monto > saldo_pendiente:
        raise HTTPException(
            status_code=400,
            detail="El monto del pago excede el saldo pendiente"
        )
    
    # Validar número de comprobante si es requerido
    if pago.metodo in ["Transferencia", "Cheque"] and not pago.numero_comprobante:
        raise HTTPException(
            status_code=400,
            detail=f"El número de comprobante es requerido para pagos con {pago.metodo}"
        )
    
    # Crear pago
    db_pago = Pagos(
        ID_Factura_Venta=pago.id_factura_venta,
        Metodo=pago.metodo,
        Monto=pago.monto,
        Numero_Comprobante=pago.numero_comprobante,
        ID_Usuario=current_user.ID_Usuario,
        Observaciones=pago.observaciones
    )
    db.add(db_pago)
    
    # Actualizar saldo del cliente
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == factura.ID_Cliente).first()
    cliente.Saldo_Actual -= pago.monto
    
    # Actualizar estado de la factura si se completó el pago
    nuevo_saldo = saldo_pendiente - pago.monto
    if nuevo_saldo == 0:
        factura.Estado = "Pagada"
    
    db.commit()
    db.refresh(db_pago)
    return db_pago

# Anular pago
@router.post("/{pago_id}/anular")
async def anular_pago(
    pago_id: int = Path(..., gt=0),
    motivo: str = Query(..., min_length=5, max_length=200),
    db: Session = Depends(get_db),
    current_user: Usuarios = Depends(get_current_user)
):
    if current_user.Rol.lower() not in ["admin", "supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    # Verificar pago
    pago = db.query(Pagos).filter(Pagos.ID_Pago == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    # Verificar factura
    factura = db.query(Facturas_Venta).filter(
        Facturas_Venta.ID_Factura_Venta == pago.ID_Factura_Venta
    ).first()
    
    # Restaurar saldo del cliente
    cliente = db.query(Clientes).filter(Clientes.ID_Cliente == factura.ID_Cliente).first()
    cliente.Saldo_Actual += pago.Monto
    
    # Actualizar estado de la factura
    if factura.Estado == "Pagada":
        factura.Estado = "Pendiente"
    
    # Eliminar pago
    db.delete(pago)
    db.commit()
    
    return {"message": "Pago anulado correctamente"}
