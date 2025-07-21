from dotenv import load_dotenv
load_dotenv()
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator


conn_str = os.getenv("SQLSERVER_CONN_STR")  
quoted = urllib.parse.quote_plus(conn_str)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quoted}"

# Creamos el engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    fast_executemany=True,   # acelera bulk insert
    echo=True               # pon True si querés ver el SQL
)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
