from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
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

def main():
    # Crear conexión a la base de datos
    SQLSERVER_CONN_STR = "mssql+pyodbc://sa:12345@localhost/Ferreteriadb?driver=ODBC+Driver+17+for+SQL+Server"
    engine = create_engine(SQLSERVER_CONN_STR)
    
    # Crear sesión
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Obtener todos los usuarios
        usuarios = db.query(Usuarios).all()
        
        # Actualizar contraseñas
        for usuario in usuarios:
            # Hashear la contraseña actual
            hashed_password = hash_password(usuario.Contraseña)
            usuario.Contraseña = hashed_password
        
        # Guardar cambios
        db.commit()
        print("Contraseñas actualizadas exitosamente")
        
    except Exception as e:
        print(f"Error al actualizar contraseñas: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 