import pyodbc
from passlib.context import CryptContext
from datetime import datetime
import os

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
    
    # Conexión directa a SQL Server
    conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Ferreteriadb;UID=sa;PWD=12345"
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        
        # Verificar si el admin ya existe
        cursor.execute("SELECT ID_Usuario FROM Usuarios WHERE Email = ?", admin_data["Email"])
        existing_user = cursor.fetchone()
        
        if not existing_user:
            # Crear nuevo admin
            hashed_password = hash_password(admin_data["Contraseña"])
            cursor.execute("""
                INSERT INTO Usuarios (Nombre, Apellido, Rol, Email, Contraseña, Estado, Creado_el, Actualizado_el)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                admin_data["Nombre"],
                admin_data["Apellido"],
                admin_data["Rol"],
                admin_data["Email"],
                hashed_password,
                admin_data["Estado"],
                admin_data["Creado_el"],
                admin_data["Actualizado_el"]
            ))
            print("Usuario administrador creado exitosamente")
        else:
            # Actualizar admin existente
            hashed_password = hash_password(admin_data["Contraseña"])
            cursor.execute("""
                UPDATE Usuarios 
                SET Contraseña = ?, Rol = ?, Actualizado_el = ?
                WHERE Email = ?
            """, (
                hashed_password,
                admin_data["Rol"],
                admin_data["Actualizado_el"],
                admin_data["Email"]
            ))
            print("Usuario administrador actualizado exitosamente")
        
        conn.commit()
        print("Proceso completado exitosamente")
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    create_admin_user() 