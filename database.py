from dotenv import load_dotenv
load_dotenv()
import os, urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

conn_str = os.getenv("SQLSERVER_CONN_STR")  
quoted = urllib.parse.quote_plus(conn_str)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={quoted}"
