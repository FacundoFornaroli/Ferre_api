from dotenv import load_dotenv
load_dotenv()
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

# Configuración por defecto si no existe el archivo .env
conn_str = os.getenv("SQLSERVER_CONN_STR")
if not conn_str:
    # Configuración por defecto para desarrollo
    conn_str = "Driver={ODBC Driver 17 for SQL Server};Server=localhost;Database=Ferreteriadb;UID=sa;PWD=12345"
    print("⚠️  Usando configuración por defecto de base de datos. Crea un archivo .env para personalizar.")

quoted = urllib.parse.quote_plus(conn_str)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quoted}"

Base = declarative_base()

# Creamos el engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    fast_executemany=True,   # acelera bulk insert
    echo=True               # pon True si querés ver el SQL
)

# Creamos la clase de sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
