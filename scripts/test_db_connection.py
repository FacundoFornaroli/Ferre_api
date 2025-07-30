import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    print("Probando conexión a la base de datos...")
    
    try:
        # Probar conexión
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            print("✅ Conexión exitosa a la base de datos")
            
            # Verificar si existe la tabla Usuarios
            result = conn.execute(text("SELECT COUNT(*) as count FROM Usuarios"))
            count = result.fetchone()[0]
            print(f"✅ Tabla Usuarios existe con {count} registros")
            
            # Verificar si existe el usuario administrador
            result = conn.execute(text("SELECT ID_Usuario, Email, Rol FROM Usuarios WHERE Email = 'juan.gonzalez@ferreteria.com'"))
            admin_user = result.fetchone()
            
            if admin_user:
                print(f"✅ Usuario administrador encontrado:")
                print(f"   ID: {admin_user[0]}")
                print(f"   Email: {admin_user[1]}")
                print(f"   Rol: {admin_user[2]}")
            else:
                print("❌ Usuario administrador NO encontrado")
                print("Creando usuario administrador...")
                create_admin_user(conn)
                
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False
    
    return True

def create_admin_user(conn):
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Datos del administrador
    admin_data = {
        "Email": "juan.gonzalez@ferreteria.com",
        "Contraseña": "admin123",
        "Nombre": "Juan",
        "Apellido": "González",
        "Rol": "admin",
        "Estado": True,
        "Creado_el": datetime.now(),
        "Actualizado_el": datetime.now()
    }
    
    try:
        # Hash de la contraseña
        hashed_password = pwd_context.hash(admin_data["Contraseña"])
        
        # Insertar usuario
        conn.execute(text("""
            INSERT INTO Usuarios (Nombre, Apellido, Rol, Email, Contraseña, Estado, Creado_el, Actualizado_el)
            VALUES (:nombre, :apellido, :rol, :email, :password, :estado, :creado_el, :actualizado_el)
        """), {
            "nombre": admin_data["Nombre"],
            "apellido": admin_data["Apellido"],
            "rol": admin_data["Rol"],
            "email": admin_data["Email"],
            "password": hashed_password,
            "estado": admin_data["Estado"],
            "creado_el": admin_data["Creado_el"],
            "actualizado_el": admin_data["Actualizado_el"]
        })
        
        conn.commit()
        print("✅ Usuario administrador creado exitosamente")
        print(f"   Email: {admin_data['Email']}")
        print(f"   Contraseña: {admin_data['Contraseña']}")
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        conn.rollback()

if __name__ == "__main__":
    test_connection() 