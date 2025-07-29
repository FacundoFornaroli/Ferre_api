from fastapi import APIRouter, Depends, HTTPException, Query, Path, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from database import get_db
from APP.schemas.Usuarios_schema import (
    UsuarioBase,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioSimple,
    UsuarioCompleta,
    UsuarioList,
    Token,
    TokenData
)
from APP.DB.Usuarios_model import Usuarios
from APP.DB.Sucursales_model import Sucursales
from sqlalchemy import func, and_, or_, case

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_aqui"  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="usuarios/login")

# Roles permitidos
ROLES_PERMITIDOS = {
    "admin": ["admin"],
    "gerente": ["admin", "gerente"],
    "vendedor": ["admin", "gerente", "vendedor"],
    "almacen": ["admin", "gerente", "almacen"],
    "contador": ["admin", "gerente", "contador"]
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Security(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(Usuarios).filter(Usuarios.Email == token_data.email).first()
    if user is None:
        raise credentials_exception
    if not user.Estado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return user

async def check_admin_role(current_user: Usuarios = Depends(get_current_user)):
    if current_user.Rol.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para esta acción"
        )
    return current_user

async def check_role_permission(required_role: str, current_user: Usuarios = Depends(get_current_user)):
    user_role = current_user.Rol.lower()
    if user_role not in ROLES_PERMITIDOS.get(required_role, []):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para esta acción"
        )
    return current_user

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    try:
        # Buscar usuario por email
        user = db.query(Usuarios).filter(Usuarios.Email == form_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar que la contraseña esté hasheada
        if not user.Contraseña.startswith("$2b$"):
            # Si no está hasheada, hashearla
            user.Contraseña = get_password_hash(user.Contraseña)
            db.commit()
        
        # Verificar contraseña
        if not verify_password(form_data.password, user.Contraseña):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Verificar estado del usuario
        if not user.Estado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Actualizar último acceso
        user.Ultimo_Acceso = datetime.utcnow()
        db.commit()
        
        # Crear token
        access_token = create_access_token(
            data={"sub": user.Email, "rol": user.Rol}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.ID_Usuario,
                "email": user.Email,
                "nombre": user.Nombre,
                "apellido": user.Apellido,
                "rol": user.Rol,
                "sucursal_id": user.ID_Sucursal
            }
        }
    except Exception as e:
        print(f"Error en login: {str(e)}")
        if "hash could not be identified" in str(e):
            # Si el error es de hash, intentar hashear la contraseña
            try:
                user.Contraseña = get_password_hash(user.Contraseña)
                db.commit()
                # Intentar verificar nuevamente
                if verify_password(form_data.password, user.Contraseña):
                    access_token = create_access_token(
                        data={"sub": user.Email, "rol": user.Rol}
                    )
                    return {
                        "access_token": access_token,
                        "token_type": "bearer",
                        "user": {
                            "id": user.ID_Usuario,
                            "email": user.Email,
                            "nombre": user.Nombre,
                            "apellido": user.Apellido,
                            "rol": user.Rol,
                            "sucursal_id": user.ID_Sucursal
                        }
                    }
            except:
                pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al procesar el login"
        )

# Obtener todos los usuarios con paginación y filtros
@router.get("/", response_model=UsuarioList)
async def get_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros a retornar"),
    estado: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    rol: Optional[str] = Query(None, description="Filtrar por rol"),
    sucursal_id: Optional[int] = Query(None, description="Filtrar por sucursal"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, apellido o email"),
    ordenar_por: Optional[str] = Query("nombre", description="Campo por el cual ordenar"),
    orden: Optional[str] = Query("asc", enum=["asc", "desc"]),
    current_user: Usuarios = Depends(check_admin_role),
    db: Session = Depends(get_db)
):
    # Query base
    query = db.query(Usuarios)
    
    # Aplicar filtros
    if estado is not None:
        query = query.filter(Usuarios.Estado == estado)
    if rol:
        query = query.filter(Usuarios.Rol == rol)
    if sucursal_id:
        query = query.filter(Usuarios.ID_Sucursal == sucursal_id)
    if buscar:
        search = f"%{buscar}%"
        query = query.filter(
            or_(
                Usuarios.Nombre.ilike(search),
                Usuarios.Apellido.ilike(search),
                Usuarios.Email.ilike(search)
            )
        )
    
    # Contar total de registros
    total = query.count()
    
    # Aplicar ordenamiento
    if ordenar_por == "nombre":
        if orden == "desc":
            query = query.order_by(Usuarios.Nombre.desc(), Usuarios.ID_Usuario.asc())
        else:
            query = query.order_by(Usuarios.Nombre.asc(), Usuarios.ID_Usuario.asc())
    elif ordenar_por == "email":
        if orden == "desc":
            query = query.order_by(Usuarios.Email.desc(), Usuarios.ID_Usuario.asc())
        else:
            query = query.order_by(Usuarios.Email.asc(), Usuarios.ID_Usuario.asc())
    elif ordenar_por == "rol":
        if orden == "desc":
            query = query.order_by(Usuarios.Rol.desc(), Usuarios.ID_Usuario.asc())
        else:
            query = query.order_by(Usuarios.Rol.asc(), Usuarios.ID_Usuario.asc())
    else:
        query = query.order_by(Usuarios.ID_Usuario.asc())
    
    # Aplicar paginación
    usuarios = query.offset(skip).limit(limit).all()
    
    # Procesar resultados
    usuarios_procesados = []
    for usuario in usuarios:
        sucursal_nombre = None
        if usuario.ID_Sucursal:
            sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == usuario.ID_Sucursal).first()
            if sucursal:
                sucursal_nombre = sucursal.Nombre
        
        usuarios_procesados.append({
            "id_usuario": usuario.ID_Usuario,
            "nombre": usuario.Nombre,
            "apellido": usuario.Apellido,
            "email": usuario.Email,
            "rol": usuario.Rol,
            "estado": usuario.Estado,
            "sucursal": sucursal_nombre
        })
    
    return {
        "total_registros": total,
        "pagina_actual": skip // limit + 1,
        "total_paginas": (total + limit - 1) // limit,
        "usuarios": usuarios_procesados
    }

# Obtener un usuario por ID
@router.get("/{usuario_id}", response_model=UsuarioCompleta)
async def get_usuario(
    usuario_id: int = Path(..., gt=0),
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.Rol not in ["Admin", "Supervisor"] and current_user.ID_Usuario != usuario_id:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    usuario = db.query(Usuarios).filter(Usuarios.ID_Usuario == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Crear nuevo usuario
@router.post("/", response_model=UsuarioCompleta)
async def create_usuario(
    usuario: UsuarioCreate,
    current_user: Usuarios = Depends(check_admin_role),
    db: Session = Depends(get_db)
):
    # Verificar si ya existe un usuario con el mismo email
    db_usuario = db.query(Usuarios).filter(Usuarios.Email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con este email"
        )
    
    # Verificar si ya existe un usuario con el mismo CUIL
    if usuario.cuil:
        db_usuario = db.query(Usuarios).filter(Usuarios.CUIL == usuario.cuil).first()
        if db_usuario:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un usuario con este CUIL"
            )
    
    # Verificar que la sucursal existe si se especifica
    if usuario.id_sucursal:
        sucursal = db.query(Sucursales).filter(
            Sucursales.ID_Sucursal == usuario.id_sucursal,
            Sucursales.Activo == True
        ).first()
        if not sucursal:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sucursal no encontrada o inactiva"
            )
    
    # Hashear la contraseña
    hashed_password = get_password_hash(usuario.contraseña)
    
    # Crear nuevo usuario
    db_usuario = Usuarios(
        Nombre=usuario.nombre,
        Apellido=usuario.apellido,
        CUIL=usuario.cuil,
        Rol=usuario.rol,
        Email=usuario.email,
        Contraseña=hashed_password,
        ID_Sucursal=usuario.id_sucursal,
        Estado=True
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    # Obtener nombre de la sucursal si existe
    sucursal_nombre = None
    if db_usuario.ID_Sucursal:
        sucursal = db.query(Sucursales).filter(Sucursales.ID_Sucursal == db_usuario.ID_Sucursal).first()
        if sucursal:
            sucursal_nombre = sucursal.Nombre
    
    return {
        "id_usuario": db_usuario.ID_Usuario,
        "nombre": db_usuario.Nombre,
        "apellido": db_usuario.Apellido,
        "email": db_usuario.Email,
        "rol": db_usuario.Rol,
        "estado": db_usuario.Estado,
        "sucursal": sucursal_nombre,
        "cuil": db_usuario.CUIL,
        "id_sucursal": db_usuario.ID_Sucursal,
        "ultimo_acceso": db_usuario.Ultimo_Acceso,
        "creado_el": db_usuario.Creado_el,
        "actualizado_el": db_usuario.Actualizado_el
    }

# Actualizar usuario
@router.put("/{usuario_id}", response_model=UsuarioCompleta)
async def update_usuario(
    usuario: UsuarioUpdate,
    usuario_id: int = Path(..., gt=0),
    current_user: Usuarios = Depends(check_admin_role),
    db: Session = Depends(get_db)
):
    # Verificar permisos
    if current_user.Rol != "Admin" and current_user.ID_Usuario != usuario_id:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    db_usuario = db.query(Usuarios).filter(Usuarios.ID_Usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Solo admin puede cambiar roles
    if usuario.rol and current_user.Rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden cambiar roles")
    
    # Verificar email único
    if usuario.email and usuario.email != db_usuario.Email:
        existe_email = db.query(Usuarios).filter(
            Usuarios.Email == usuario.email,
            Usuarios.ID_Usuario != usuario_id
        ).first()
        if existe_email:
            raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Verificar CUIL único
    if usuario.cuil and usuario.cuil != db_usuario.CUIL:
        existe_cuil = db.query(Usuarios).filter(
            Usuarios.CUIL == usuario.cuil,
            Usuarios.ID_Usuario != usuario_id
        ).first()
        if existe_cuil:
            raise HTTPException(status_code=400, detail="CUIL ya registrado")
    
    # Verificar sucursal
    if usuario.id_sucursal:
        sucursal = db.query(Sucursales).filter(
            Sucursales.ID_Sucursal == usuario.id_sucursal,
            Sucursales.Activo == True
        ).first()
        if not sucursal:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada o inactiva")
    
    # Actualizar contraseña si se proporciona
    if usuario.contraseña:
        usuario.contraseña = get_password_hash(usuario.contraseña)
    
    # Actualizar campos
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key.capitalize(), value)
    
    db_usuario.Actualizado_el = datetime.now()
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Cambiar estado del usuario (activar/desactivar)
@router.patch("/{usuario_id}/estado")
async def change_usuario_estado(
    usuario_id: int = Path(..., gt=0),
    estado: bool = Query(..., description="Nuevo estado del usuario"),
    current_user: Usuarios = Depends(check_admin_role),
    db: Session = Depends(get_db)
):
    if current_user.Rol != "Admin":
        raise HTTPException(status_code=403, detail="Solo administradores pueden cambiar estados")
    
    if usuario_id == current_user.ID_Usuario:
        raise HTTPException(status_code=400, detail="No puede cambiar su propio estado")
    
    db_usuario = db.query(Usuarios).filter(Usuarios.ID_Usuario == usuario_id).first()
    if not db_usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_usuario.Estado = estado
    db_usuario.Actualizado_el = datetime.now()
    db.commit()
    
    return {"message": f"Usuario {'activado' if estado else 'desactivado'} correctamente"}

# Cambiar contraseña propia
@router.post("/cambiar-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not verify_password(current_password, current_user.Contraseña):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    current_user.Contraseña = get_password_hash(new_password)
    current_user.Actualizado_el = datetime.now()
    db.commit()
    
    return {"message": "Contraseña actualizada correctamente"}

# Obtener estadísticas de usuarios
@router.get("/estadisticas", response_model=dict)
async def get_estadisticas_usuarios(
    current_user: Usuarios = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.Rol not in ["Admin", "Supervisor"]:
        raise HTTPException(status_code=403, detail="No tiene permisos para esta acción")
    
    total = db.query(func.count(Usuarios.ID_Usuario)).scalar()
    activos = db.query(func.count(Usuarios.ID_Usuario)).filter(Usuarios.Estado == True).scalar()
    
    # Usuarios por rol
    por_rol = db.query(
        Usuarios.Rol,
        func.count(Usuarios.ID_Usuario).label('total')
    ).group_by(Usuarios.Rol).all()
    
    # Usuarios por sucursal
    por_sucursal = db.query(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre,
        func.count(Usuarios.ID_Usuario).label('total_usuarios')
    ).join(Usuarios).group_by(
        Sucursales.ID_Sucursal,
        Sucursales.Nombre
    ).all()
    
    # Últimos accesos
    ultimos_accesos = db.query(
        func.count(Usuarios.ID_Usuario).label('total'),
        func.sum(case((Usuarios.Ultimo_Acceso >= datetime.now() - timedelta(days=7), 1), else_=0)).label('ultima_semana'),
        func.sum(case((Usuarios.Ultimo_Acceso >= datetime.now() - timedelta(days=30), 1), else_=0)).label('ultimo_mes')
    ).first()
    
    return {
        "total_usuarios": total,
        "usuarios_activos": activos,
        "por_rol": [
            {"rol": r.Rol, "total": r.total}
            for r in por_rol
        ],
        "por_sucursal": [
            {
                "id": s.ID_Sucursal,
                "nombre": s.Nombre,
                "total_usuarios": s.total_usuarios
            }
            for s in por_sucursal
        ],
        "accesos": {
            "ultima_semana": ultimos_accesos.ultima_semana or 0,
            "ultimo_mes": ultimos_accesos.ultimo_mes or 0
        }
    }
