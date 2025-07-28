from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
import time
import logging
import traceback

# Importar todos los routers
from APP.routers.Categorias_router import router as categorias_router
from APP.routers.Unidades_de_medida_router import router as unidades_medida_router
from APP.routers.Sucursales_router import router as sucursales_router
from APP.routers.Usuarios_router import router as usuarios_router
from APP.routers.Productos_router import router as productos_router
from APP.routers.Clientes_router import router as clientes_router
from APP.routers.Proveedores_router import router as proveedores_router
from APP.routers.Inventario_router import router as inventario_router
from APP.routers.Facturas_Venta_router import router as facturas_venta_router
from APP.routers.Detalles_Factura_Venta_router import router as detalles_factura_router
from APP.routers.Pagos_router import router as pagos_router
from APP.routers.Ordenes_Compra_router import router as ordenes_compra_router
from APP.routers.Detalle_OC_router import router as detalle_oc_router
from APP.routers.Movimientos_Inventario_router import router as movimientos_router
from APP.routers.Garantias_router import router as garantias_router
from APP.routers.Descuentos_router import router as descuentos_router
from APP.routers.Productos_Descuentos_router import router as productos_descuentos_router
from APP.routers.Devoluciones_router import router as devoluciones_router
from APP.routers.Transferencias_Sucursales_router import router as transferencias_router
from APP.routers.Detalles_Transferencias_router import router as detalles_transferencias_router
from APP.routers.Auditoria_Cambios_router import router as auditoria_router

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
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        logger.info(
            f"Method: {request.method} - Path: {request.url.path} - "
            f"Status: {response.status_code} - Duration: {duration:.2f}s"
        )
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Method: {request.method} - Path: {request.url.path} - "
            f"Error: {str(e)} - Duration: {duration:.2f}s\n"
            f"Traceback: {traceback.format_exc()}"
        )
        raise

# Manejadores de errores globales
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Error de validación",
            "errors": exc.errors()
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    logger.error(f"Integrity error: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": "Error de integridad en la base de datos",
            "message": str(exc)
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error en la base de datos",
            "message": str(exc)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Error interno del servidor",
            "message": str(exc)
        }
    )

# Incluir todos los routers
app.include_router(categorias_router)
app.include_router(unidades_medida_router)
app.include_router(sucursales_router)
app.include_router(usuarios_router)
app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(proveedores_router)
app.include_router(inventario_router)
app.include_router(facturas_venta_router)
app.include_router(detalles_factura_router)
app.include_router(pagos_router)
app.include_router(ordenes_compra_router)
app.include_router(detalle_oc_router)
app.include_router(movimientos_router)
app.include_router(garantias_router)
app.include_router(descuentos_router)
app.include_router(productos_descuentos_router)
app.include_router(devoluciones_router)
app.include_router(transferencias_router)
app.include_router(detalles_transferencias_router)
app.include_router(auditoria_router)

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
