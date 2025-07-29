# API de Ferretería

Sistema de gestión completo para ferretería desarrollado con FastAPI y SQL Server.

## 🚀 Características

- **Gestión de Inventario**: Control de stock, movimientos, alertas de stock bajo
- **Ventas**: Facturación, pagos, devoluciones
- **Compras**: Órdenes de compra, proveedores
- **Clientes**: Gestión completa de clientes
- **Usuarios**: Sistema de autenticación y autorización por roles
- **Sucursales**: Gestión multi-sucursal
- **Transferencias**: Entre sucursales
- **Auditoría**: Registro de cambios
- **Reportes**: Estadísticas y análisis

## 📋 Requisitos

- Python 3.8+
- SQL Server 2019+
- ODBC Driver 17 for SQL Server

## 🛠️ Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Ferre_api
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
- Ejecutar el script `SQL SERVER/Estructura_Ferreteriadb.sql` en SQL Server
- Ejecutar el script `SQL SERVER/Insercion_datos_Ferreteriadb.sql` para datos de prueba

5. **Crear usuario administrador**
```bash
# Opción 1: Ejecutar script SQL directamente en SQL Server Management Studio
# Abrir scripts/insert_admin.sql y ejecutarlo

# Opción 2: Usar el script Python (si las credenciales están correctas)
python scripts/create_admin_sqlalchemy.py
```

## 🔑 Credenciales de Administrador

**Email:** `juan.gonzalez@ferreteria.com`  
**Contraseña:** `admin123`

## 🚀 Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en: http://localhost:8000

## 📚 Documentación de la API

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 👥 Roles de Usuario

- **admin**: Acceso completo a todas las funcionalidades
- **gerente**: Gestión de ventas, inventario y reportes
- **vendedor**: Ventas y consultas básicas
- **almacen**: Gestión de inventario y transferencias
- **contador**: Reportes financieros y auditoría

## 📁 Estructura del Proyecto

```
Ferre_api/
├── APP/
│   ├── DB/                 # Modelos SQLAlchemy
│   ├── routers/           # Endpoints de la API
│   └── schemas/           # Esquemas Pydantic
├── SQL SERVER/            # Scripts de base de datos
├── scripts/              # Scripts de utilidad
├── logs/                 # Archivos de log
├── main.py              # Aplicación principal
├── database.py          # Configuración de BD
└── requirements.txt     # Dependencias
```

## 🔧 Configuración

### Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Configuración de la base de datos SQL Server
SQLSERVER_CONN_STR=Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=Ferreteriadb;UID=sa;PWD=12345

# Configuración de JWT
SECRET_KEY=tu_clave_secreta_aqui_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de la aplicación
ENVIRONMENT=development
DEBUG=True
```

## 📊 Endpoints Principales

### Autenticación
- `POST /usuarios/login` - Iniciar sesión

### Gestión de Usuarios
- `GET /usuarios/` - Listar usuarios (requiere admin)
- `POST /usuarios/` - Crear usuario (requiere admin)
- `PUT /usuarios/{id}` - Actualizar usuario (requiere admin)

### Productos
- `GET /productos/` - Listar productos
- `POST /productos/` - Crear producto
- `PUT /productos/{id}` - Actualizar producto

### Inventario
- `GET /inventario/` - Listar inventario
- `GET /inventario/stock-bajo` - Productos con stock bajo

### Ventas
- `GET /facturas-venta/` - Listar facturas
- `POST /facturas-venta/` - Crear factura

### Clientes
- `GET /clientes/` - Listar clientes
- `POST /clientes/` - Crear cliente

## 🐛 Solución de Problemas

### Error de conexión a la base de datos
1. Verificar que SQL Server esté ejecutándose
2. Verificar las credenciales en el archivo `.env`
3. Verificar que el ODBC Driver 17 esté instalado

### Error de autenticación
1. Ejecutar el script `scripts/insert_admin.sql` en SQL Server
2. Verificar que el usuario administrador exista en la base de datos

### Logs excesivos
- Los logs se guardan en `logs/app.log` con rotación automática
- El archivo anterior se movió a `logs/app_old.log`

## 🔒 Seguridad

- **JWT**: Autenticación basada en tokens
- **Roles**: Autorización por roles de usuario
- **Validación**: Validación de datos con Pydantic
- **Logging**: Registro de todas las operaciones

## 📈 Monitoreo

- **Logs**: Archivos de log con rotación automática
- **Auditoría**: Registro de cambios en la base de datos
- **Estadísticas**: Endpoints para reportes y análisis

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o consultas, contactar al equipo de desarrollo. 