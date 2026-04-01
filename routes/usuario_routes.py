from fastapi import APIRouter, Depends
from models.usuario import UsuarioCreate, UsuarioUpdate
from services.usuario_service import *
from schemas.usuario_schema import usuario_schema, usuarios_schema

# 🔐 JWT
from auth.jwt_handler import crear_token
from auth.dependencies import get_current_user

router = APIRouter()

# =========================
# 🔐 LOGIN
# =========================
@router.post("/login")
def login(correo: str, password: str):
    usuario = login_usuario(correo, password)

    token = crear_token({
        "id": str(usuario["_id"]),
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# =========================
# 👤 CRUD USUARIOS
# =========================

# 🔓 Público (registro)
@router.post("/usuarios")
def crear(data: UsuarioCreate):
    id = crear_usuario(data)
    return {"ok": True, "id": id}

# 🔐 Protegidos
@router.get("/usuarios")
def listar(user=Depends(get_current_user)):
    return usuarios_schema(listar_usuarios())

@router.get("/usuarios/{usuario_id}")
def obtener(usuario_id: str, user=Depends(get_current_user)):
    return usuario_schema(obtener_usuario(usuario_id))

@router.put("/usuarios/{usuario_id}")
def actualizar(usuario_id: str, data: UsuarioUpdate, user=Depends(get_current_user)):
    actualizar_usuario(usuario_id, data)
    return {"ok": True}

@router.delete("/usuarios/{usuario_id}")
def eliminar(usuario_id: str, user=Depends(get_current_user)):
    eliminar_usuario(usuario_id)
    return {"ok": True}

@router.get("/usuarios/buscar/")
def buscar(correo: str = None, ci: str = None, user=Depends(get_current_user)):
    return usuario_schema(buscar_usuario(correo, ci))