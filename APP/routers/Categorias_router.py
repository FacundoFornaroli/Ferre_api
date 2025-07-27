from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from ...database import get_db  # Un nivel más arriba con tres puntos
from ..schemas.Categorias_schema import CategoriaBase, CategoriaCreate, CategoriaUpdate, CategoriaSimple, CategoriaCompleta, CategoriaList, CategoriaEstadisticas
from ..DB.Categorias_model import Categorias  # Note que también es 'Categorias', no 'Categoria'
from sqlalchemy import func
