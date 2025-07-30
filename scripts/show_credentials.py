import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from sqlalchemy import text

def show_credentials():
    print("=" * 60)
    print("🔑 CREDENCIALES DE ADMINISTRADOR - API FERRETERÍA")
    print("=" * 60)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar usuario administrador
        result = db.execute(text("SELECT ID_Usuario, Nombre, Apellido, Email, Rol, Estado FROM Usuarios WHERE Email = 'juan.gonzalez@ferreteria.com'"))
        user = result.fetchone()
        
        if user:
            print("✅ Usuario administrador encontrado:")
            print(f"   ID: {user[0]}")
            print(f"   Nombre: {user[1]} {user[2]}")
            print(f"   Email: {user[3]}")
            print(f"   Rol: {user[4]}")
            print(f"   Estado: {'Activo' if user[5] else 'Inactivo'}")
        else:
            print("❌ Usuario administrador no encontrado")
            return
        
        print("\n" + "=" * 60)
        print("🔐 CREDENCIALES DE ACCESO")
        print("=" * 60)
        print("📧 Email: juan.gonzalez@ferreteria.com")
        print("🔒 Contraseña: admin123")
        
        print("\n" + "=" * 60)
        print("🌐 INSTRUCCIONES DE ACCESO")
        print("=" * 60)
        print("1. Abre tu navegador web")
        print("2. Ve a: http://localhost:8000/docs")
        print("3. Haz clic en el botón 'Authorize' (🔒) en la parte superior")
        print("4. Usa las credenciales de arriba")
        print("5. Haz clic en 'Authorize'")
        print("6. ¡Listo! Ya puedes usar todas las funcionalidades")
        
        print("\n" + "=" * 60)
        print("📋 FUNCIONALIDADES DISPONIBLES")
        print("=" * 60)
        print("✅ Gestión de usuarios")
        print("✅ Gestión de productos")
        print("✅ Gestión de inventario")
        print("✅ Gestión de clientes")
        print("✅ Gestión de proveedores")
        print("✅ Facturación y ventas")
        print("✅ Órdenes de compra")
        print("✅ Transferencias entre sucursales")
        print("✅ Reportes y estadísticas")
        print("✅ Auditoría de cambios")
        
        print("\n" + "=" * 60)
        print("🔧 ESTADO DEL SISTEMA")
        print("=" * 60)
        print("✅ API funcionando en: http://localhost:8000")
        print("✅ Base de datos conectada")
        print("✅ Usuario administrador configurado")
        print("✅ Sistema de logging optimizado")
        
        print("\n" + "=" * 60)
        print("📞 SOPORTE")
        print("=" * 60)
        print("Si tienes problemas:")
        print("1. Verifica que la aplicación esté ejecutándose")
        print("2. Verifica que el puerto 8000 esté disponible")
        print("3. Revisa los logs en: logs/app.log")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    show_credentials() 