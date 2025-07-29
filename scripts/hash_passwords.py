from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from datetime import datetime
import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Base
from APP.DB.Usuarios_model import Usuarios

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def create_admin_user(db):
    # Datos del administrador por defecto
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
    
    # Verificar si el admin ya existe
    admin = db.query(Usuarios).filter(Usuarios.Email == admin_data["Email"]).first()
    
    if not admin:
        # Crear nuevo admin
        admin = Usuarios(
            Email=admin_data["Email"],
            Contraseña=hash_password(admin_data["Contraseña"]),
            Nombre=admin_data["Nombre"],
            Apellido=admin_data["Apellido"],
            Rol=admin_data["Rol"],
            Estado=admin_data["Estado"],
            Creado_el=admin_data["Creado_el"],
            Actualizado_el=admin_data["Actualizado_el"]
        )
        db.add(admin)
        db.commit()
        print("Usuario administrador creado exitosamente")
    else:
        # Actualizar contraseña del admin existente
        admin.Contraseña = hash_password(admin_data["Contraseña"])
        db.commit()
        print("Contraseña del administrador actualizada exitosamente")

def main():
    # Crear conexión a la base de datos
    SQLSERVER_CONN_STR = "mssql+pyodbc://sa:12345@localhost/Ferreteriadb?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(SQLSERVER_CONN_STR)
    
    # Crear sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Crear o actualizar usuario administrador
        create_admin_user(db)
        
        # Obtener todos los usuarios excepto el admin
        usuarios = db.query(Usuarios).filter(
            Usuarios.Email != "juan.gonzalez@ferreteria.com"
        ).all()
        
        # Actualizar contraseñas de otros usuarios
        for usuario in usuarios:
            if usuario.Contraseña and not usuario.Contraseña.startswith("$2b$"):
                # Solo hashear si la contraseña no está ya hasheada
                hashed_password = hash_password(usuario.Contraseña)
                usuario.Contraseña = hashed_password
                print(f"Contraseña actualizada para usuario: {usuario.Email}")
        
        # Guardar cambios
        db.commit()
        print("Proceso completado exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 