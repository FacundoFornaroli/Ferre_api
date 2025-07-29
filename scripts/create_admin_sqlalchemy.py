import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def create_admin_user():
    # Datos del administrador por defecto
    admin_data = {
        "Email": "juan.gonzalez@ferreteria.com",
        "Contraseña": "admin123",
        "Nombre": "Juan",
        "Apellido": "González",
        "Rol": "admin",  # En minúsculas
        "Estado": True,
        "Creado_el": datetime.now(),
        "Actualizado_el": datetime.now()
    }
    
    # Usar la misma configuración que la aplicación principal
    SQLSERVER_CONN_STR = "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=Ferreteriadb;UID=sa;PWD=12345"
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={SQLSERVER_CONN_STR}")
    
    # Crear sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Verificar si el admin ya existe
        result = db.execute(text("SELECT ID_Usuario FROM Usuarios WHERE Email = :email"), {"email": admin_data["Email"]})
        existing_user = result.fetchone()
        
        if not existing_user:
            # Crear nuevo admin
            hashed_password = hash_password(admin_data["Contraseña"])
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
            print("Usuario administrador creado exitosamente")
        else:
            # Actualizar admin existente
            hashed_password = hash_password(admin_data["Contraseña"])
            db.execute(text("""
                UPDATE Usuarios 
                SET Contraseña = :password, Rol = :rol, Actualizado_el = :actualizado_el
                WHERE Email = :email
            """), {
                "password": hashed_password,
                "rol": admin_data["Rol"],
                "actualizado_el": admin_data["Actualizado_el"],
                "email": admin_data["Email"]
            })
            print("Usuario administrador actualizado exitosamente")
        
        db.commit()
        print("Proceso completado exitosamente")
        print(f"Credenciales de administrador:")
        print(f"Email: {admin_data['Email']}")
        print(f"Contraseña: {admin_data['Contraseña']}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 