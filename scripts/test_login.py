import sys
import os
from datetime import datetime

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from sqlalchemy import text
from passlib.context import CryptContext
from jose import jwt

def test_login():
    print("Probando login del usuario administrador...")
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Datos de prueba
    email = "juan.gonzalez@ferreteria.com"
    password = "admin123"
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Buscar usuario
        result = db.execute(text("SELECT ID_Usuario, Nombre, Apellido, Email, Contraseña, Rol, Estado FROM Usuarios WHERE Email = :email"), {"email": email})
        user = result.fetchone()
        
        if not user:
            print("❌ Usuario no encontrado")
            return
        
        print(f"✅ Usuario encontrado:")
        print(f"   ID: {user[0]}")
        print(f"   Nombre: {user[1]} {user[2]}")
        print(f"   Email: {user[3]}")
        print(f"   Rol: {user[5]}")
        print(f"   Estado: {user[6]}")
        print(f"   Contraseña: {user[4][:20]}...")
        
        # Verificar contraseña
        if pwd_context.verify(password, user[4]):
            print("✅ Contraseña válida")
            
            # Crear token (simulando el endpoint)
            SECRET_KEY = "tu_clave_secreta_aqui"
            ALGORITHM = "HS256"
            ACCESS_TOKEN_EXPIRE_MINUTES = 30
            
            expire = datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            to_encode = {"sub": user[3], "rol": user[5], "exp": expire}
            access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
            
            print("✅ Token creado exitosamente")
            print(f"   Token: {access_token[:50]}...")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user[0],
                    "email": user[3],
                    "nombre": user[1],
                    "apellido": user[2],
                    "rol": user[5],
                    "sucursal_id": None
                }
            }
        else:
            print("❌ Contraseña inválida")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    result = test_login()
    if result:
        print("\n🎉 Login exitoso!")
        print("Credenciales válidas:")
        print(f"   Email: juan.gonzalez@ferreteria.com")
        print(f"   Contraseña: admin123")
        print("\n🔑 Puedes usar estas credenciales en:")
        print("   http://localhost:8000/docs")
    else:
        print("\n❌ Login fallido") 