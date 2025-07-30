import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from sqlalchemy import text
from passlib.context import CryptContext

def create_admin_user():
    print("Creando usuario administrador...")
    
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
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si el usuario ya existe
        result = db.execute(text("SELECT ID_Usuario FROM Usuarios WHERE Email = :email"), {"email": admin_data["Email"]})
        existing_user = result.fetchone()
        
        if existing_user:
            print("✅ Usuario administrador ya existe")
            print(f"   Email: {admin_data['Email']}")
            print(f"   Contraseña: {admin_data['Contraseña']}")
            return
        
        # Hash de la contraseña
        hashed_password = pwd_context.hash(admin_data["Contraseña"])
        
        # Insertar usuario
        db.execute(text("""
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
        
        db.commit()
        print("✅ Usuario administrador creado exitosamente")
        print(f"   Email: {admin_data['Email']}")
        print(f"   Contraseña: {admin_data['Contraseña']}")
        print("\n🔑 Ahora puedes usar estas credenciales para hacer login en:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 