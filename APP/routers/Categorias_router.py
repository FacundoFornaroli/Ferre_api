from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..schemas.Categorias_schema import CategoriaBase, CategoriaCreate, CategoriaUpdate, CategoriaSimple, CategoriaCompleta, CategoriaList, CategoriaEstadisticas
from ..models.Categorias_model import categorias
from sqlalchemy import func
