# 🏪 Ferre API - Sistema de Gestión para Ferretería

## 👨‍💻 Sobre el Desarrollador

¡Hola! Soy un **desarrollador principiante** apasionado por aprender y mejorar mis habilidades en programación. Este proyecto representa mi viaje de aprendizaje en el desarrollo de APIs con FastAPI, bases de datos SQL Server y sistemas de gestión empresarial.

### 🎯 Mi Enfoque de Aprendizaje
- **Aprendizaje Continuo**: Este proyecto está en **desarrollo activo** y constante evolución
- **Experimentación**: Pruebo diferentes enfoques y mejores prácticas
- **Mejora Constante**: Cada día aprendo algo nuevo y aplico esos conocimientos
- **Código Abierto**: Comparto mi progreso para recibir feedback y ayudar a otros principiantes

### 🚧 Estado del Proyecto
**⚠️ IMPORTANTE**: Este es un proyecto en **desarrollo continuo**. Como principiante, estoy constantemente:
- Aprendiendo nuevas tecnologías
- Refactorizando código
- Implementando mejores prácticas
- Corrigiendo errores y mejorando funcionalidades

## 📋 Descripción del Proyecto

**Ferre API** es un sistema de gestión integral para ferreterías desarrollado con **FastAPI** y **SQL Server**. El proyecto nació de mi interés por aprender desarrollo backend y gestión de bases de datos empresariales.

### 🎯 Objetivos del Proyecto
- **Aprendizaje Práctico**: Aplicar conocimientos de FastAPI, SQLAlchemy y SQL Server
- **Sistema Completo**: Crear una solución real para gestión de inventario y ventas
- **Mejores Prácticas**: Implementar patrones de diseño y arquitectura limpia
- **Documentación**: Aprender a documentar código y APIs correctamente

## 🛠️ Tecnologías Utilizadas

### Backend
- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para Python
- **Pydantic** - Validación de datos y serialización
- **JWT** - Autenticación y autorización

### Base de Datos
- **SQL Server** - Sistema de gestión de bases de datos
- **ODBC Driver** - Conectividad con SQL Server

### Herramientas de Desarrollo
- **Python 3.13** - Lenguaje de programación
- **Uvicorn** - Servidor ASGI
- **Git** - Control de versiones

## 🏗️ Arquitectura del Sistema

### Módulos Principales
```
Ferre_api/
├── APP/
│   ├── DB/                 # Modelos de base de datos
│   ├── routers/           # Endpoints de la API
│   └── schemas/           # Esquemas Pydantic
├── SQL SERVER/            # Scripts de base de datos
├── scripts/              # Scripts de utilidad
├── logs/                 # Archivos de log
├── main.py              # Aplicación principal
├── database.py          # Configuración de BD
└── requirements.txt     # Dependencias
```

### Funcionalidades Implementadas
- **Gestión de Usuarios**: Autenticación, roles y permisos
- **Gestión de Productos**: CRUD completo con categorías
- **Inventario**: Control de stock por sucursal
- **Ventas**: Facturación y gestión de clientes
- **Compras**: Órdenes de compra y proveedores
- **Pagos**: Gestión de pagos y cuentas por cobrar
- **Auditoría**: Registro de cambios en el sistema
- **Reportes**: Estadísticas y análisis de datos

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.13+
- SQL Server (local o remoto)
- ODBC Driver 17 for SQL Server

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd Ferre_api
```

2. **Crear entorno virtual**
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**
- Ejecutar el script `SQL SERVER/Estructura_Ferreteriadb.sql` en SQL Server
- Crear archivo `.env` con las credenciales de conexión

5. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
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

6. **Ejecutar el servidor**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentación de la API

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

## 🎓 Mi Proceso de Aprendizaje

### Lo que he aprendido hasta ahora:
- **FastAPI**: Desarrollo de APIs RESTful modernas
- **SQLAlchemy**: Mapeo objeto-relacional
- **SQL Server**: Gestión de bases de datos empresariales
- **JWT**: Implementación de autenticación segura
- **Pydantic**: Validación y serialización de datos
- **Arquitectura**: Patrones de diseño y organización de código

### Lo que estoy aprendiendo actualmente:
- **Testing**: Implementación de pruebas unitarias e integración
- **Documentación**: Mejores prácticas para documentar APIs
- **Performance**: Optimización de consultas y rendimiento
- **Deployment**: Despliegue en producción

### Lo que planeo aprender:
- **Docker**: Containerización de la aplicación
- **CI/CD**: Integración y despliegue continuo
- **Microservicios**: Arquitectura distribuida
- **Cloud**: Despliegue en servicios cloud

## 🤝 Contribución

Como principiante, **agradezco enormemente** cualquier feedback, sugerencia o contribución:

1. **Issues**: Reportar bugs o sugerir mejoras
2. **Pull Requests**: Contribuciones de código
3. **Discusiones**: Compartir conocimientos y experiencias
4. **Documentación**: Mejorar la documentación existente

### Cómo contribuir:
1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto y Soporte

- **GitHub**: [Tu perfil de GitHub]
- **Email**: [Tu email]
- **LinkedIn**: [Tu perfil de LinkedIn]

### Para otros principiantes:
Si también estás aprendiendo desarrollo backend, ¡me encantaría conectarme contigo! Podemos compartir experiencias, resolver problemas juntos y aprender de nuestros errores.

## 🙏 Agradecimientos

- **Comunidad de FastAPI**: Por la excelente documentación y soporte
- **Stack Overflow**: Por ayudarme a resolver innumerables problemas
- **GitHub**: Por proporcionar una plataforma para compartir código
- **Todos los que han contribuido**: Por su paciencia y enseñanzas

---

**Nota**: Este proyecto es el resultado de mi pasión por aprender. Cada línea de código representa un paso en mi viaje de aprendizaje. ¡Gracias por ser parte de esta aventura! 🚀 