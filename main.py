from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
import time
import logging

# Importar todos los routers
from APP.routers import (
    Categorias_router,
    Unidades_de_medida_router,
    Sucursales_router,
    Usuarios_router,
    Productos_router,
    Clientes_router,
    Proveedores_router,
    Inventario_router,
    Facturas_Venta_router,
    Detalles_Factura_Venta_router,
    Pagos_router,
    Ordenes_Compra_router,
    Detalle_OC_router,
    Movimientos_Inventario_router,
    Garantias_router,
    Descuentos_router,
    Productos_Descuentos_router,
    Devoluciones_router,
    Transferencias_Sucursales_router,
    Detalles_Transferencias_router,
    Auditoria_Cambios_router
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Ferretería API",
    description="""
    API REST para el sistema de gestión de ferretería.
    Incluye manejo de:
    * Inventario
    * Ventas
    * Compras
    * Clientes
    * Proveedores
    * Usuarios
    * Y más...
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"Method: {request.method} - Path: {request.url.path} - "
        f"Status: {response.status_code} - Duration: {duration:.2f}s"
    )
    
    return response

# Manejadores de errores globales
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": exc.errors()
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Error de integridad en la base de datos",
            "message": str(exc)
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error en la base de datos",
            "message": str(exc)
        }
    )

# Incluir todos los routers
app.include_router(Categorias_router.router)
app.include_router(Unidades_de_medida_router.router)
app.include_router(Sucursales_router.router)
app.include_router(Usuarios_router.router)
app.include_router(Productos_router.router)
app.include_router(Clientes_router.router)
app.include_router(Proveedores_router.router)
app.include_router(Inventario_router.router)
app.include_router(Facturas_Venta_router.router)
app.include_router(Detalles_Factura_Venta_router.router)
app.include_router(Pagos_router.router)
app.include_router(Ordenes_Compra_router.router)
app.include_router(Detalle_OC_router.router)
app.include_router(Movimientos_Inventario_router.router)
app.include_router(Garantias_router.router)
app.include_router(Descuentos_router.router)
app.include_router(Productos_Descuentos_router.router)
app.include_router(Devoluciones_router.router)
app.include_router(Transferencias_Sucursales_router.router)
app.include_router(Detalles_Transferencias_router.router)
app.include_router(Auditoria_Cambios_router.router)

# Endpoint de estado/salud
@app.get("/", tags=["Estado"])
async def root():
    return {
        "status": "online",
        "timestamp": datetime.now(),
        "version": app.version
    }

# Endpoint para información del sistema
@app.get("/info", tags=["Estado"])
async def info():
    return {
        "app_name": "Ferretería API",
        "version": app.version,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "environment": "development",  # Cambiar según ambiente
        "database": "SQL Server",
        "timestamp": datetime.now()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Solo en desarrollo
        log_level="info"
    )
