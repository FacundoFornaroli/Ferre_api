import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from sqlalchemy import text
from passlib.context import CryptContext

def update_admin_password():
    print("Actualizando contraseña del usuario administrador...")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Datos del administrador
    admin_data = {
        "Email": "juan.gonzalez@ferreteria.com",
        "Contraseña": "admin123",
        "Rol": "admin"
    }
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si el usuario existe
        result = db.execute(text("SELECT ID_Usuario, Contraseña, Rol FROM Usuarios WHERE Email = :email"), {"email": admin_data["Email"]})
        user = result.fetchone()
        
        if not user:
            print("❌ Usuario administrador no encontrado")
            return
        
        print(f"✅ Usuario encontrado:")
        print(f"   ID: {user[0]}")
        print(f"   Email: {admin_data['Email']}")
        print(f"   Rol actual: {user[2]}")
        print(f"   Contraseña actual: {user[1][:20]}...")
        
        # Hash de la nueva contraseña
        hashed_password = pwd_context.hash(admin_data["Contraseña"])
        print(f"   Nueva contraseña hasheada: {hashed_password[:20]}...")
        
        # Verificar si la contraseña actual es válida
        if pwd_context.verify(admin_data["Contraseña"], user[1]):
            print("✅ La contraseña actual es válida")
        else:
            print("❌ La contraseña actual NO es válida, actualizando...")
        
        # Actualizar usuario
        db.execute(text("""
            UPDATE Usuarios 
            SET Contraseña = :password, Rol = :rol, Actualizado_el = :actualizado_el
            WHERE Email = :email
        """), {
            "password": hashed_password,
            "rol": admin_data["Rol"],
            "actualizado_el": datetime.now(),
            "email": admin_data["Email"]
        })
        
        db.commit()
        print("✅ Usuario administrador actualizado exitosamente")
        print(f"   Email: {admin_data['Email']}")
        print(f"   Contraseña: {admin_data['Contraseña']}")
        print(f"   Rol: {admin_data['Rol']}")
        print("\n🔑 Ahora puedes usar estas credenciales para hacer login en:")
        print("   http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error actualizando usuario administrador: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin_password() 