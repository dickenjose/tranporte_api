from fastapi import APIRouter, Depends
from pydantic import BaseModel  # 👈 NUEVO

from models.usuario import UsuarioCreate, UsuarioUpdate
from services.usuario_service import *
from schemas.usuario_schema import usuario_schema, usuarios_schema

# 🔐 JWT
from auth.jwt_handler import crear_token
from auth.dependencies import get_current_user

router = APIRouter()

# =========================
# 🆕 MODELO PARA LOGIN
# =========================
class LoginRequest(BaseModel):
    correo: str
    password: str


# =========================
# 🔐 LOGIN MEJORADO (CORREGIDO)
# =========================
@router.post("/login")
def login(data: LoginRequest):  # 👈 CAMBIO AQUÍ
    try:
        correo = data.correo
        password = data.password

        print(f"🔐 Intento de login → {correo}")

        usuario = login_usuario(correo, password)

        # ❌ Usuario no encontrado o contraseña incorrecta
        if not usuario:
            return {
                "ok": False,
                "mensaje": "Credenciales incorrectas"
            }

        # 🔐 Generar token
        token = crear_token({
            "id": str(usuario["_id"]),
            "correo": usuario["correo"],
            "rol": usuario["rol"]
        })

        print(f"✅ Login exitoso → {correo}")

        return {
            "ok": True,
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": str(usuario["_id"]),
                "correo": usuario["correo"],
                "rol": usuario["rol"]
            }
        }

    except Exception as e:
        print("❌ Error en login:", e)
        return {
            "ok": False,
            "mensaje": "Error interno del servidor"
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