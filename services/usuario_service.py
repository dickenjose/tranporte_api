from config.database import usuarios
from fastapi import HTTPException
from bson import ObjectId
import bcrypt
from datetime import datetime


def crear_usuario(data):
    if usuarios.find_one({"correo": data.correo}):
        raise HTTPException(400, "Correo ya existe")

    password_hash = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    nuevo = {
        "nombre": data.nombre,
        "ci": data.ci,
        "telefono": data.telefono,
        "correo": data.correo,
        "password": password_hash,
        "rol": data.rol,
        "perfil": data.perfil.dict() if data.perfil else {},
        "estado": "activo",
        "fecha_creacion": datetime.utcnow()
    }
    result = usuarios.insert_one(nuevo)
    return str(result.inserted_id)


def listar_usuarios():
    return usuarios.find()


def obtener_usuario(usuario_id):
    usuario = usuarios.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")
    return usuario


def actualizar_usuario(usuario_id, data):
    usuario = obtener_usuario(usuario_id)

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if "password" in update_data:
        update_data["password"] = bcrypt.hashpw(update_data["password"].encode(), bcrypt.gensalt()).decode()

    if "correo" in update_data and update_data["correo"] != usuario["correo"]:
        if usuarios.find_one({"correo": update_data["correo"]}):
            raise HTTPException(400, "Correo ya existe")

    if "ci" in update_data and update_data["ci"] != usuario["ci"]:
        if usuarios.find_one({"ci": update_data["ci"]}):
            raise HTTPException(400, "CI ya existe")

    usuarios.update_one({"_id": ObjectId(usuario_id)}, {"$set": update_data})


def eliminar_usuario(usuario_id):
    result = usuarios.delete_one({"_id": ObjectId(usuario_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Usuario no encontrado")


def buscar_usuario(correo=None, ci=None):
    query = {}
    if correo:
        query["correo"] = correo
    if ci:
        query["ci"] = ci

    if not query:
        raise HTTPException(400, "Se requiere correo o CI")

    usuario = usuarios.find_one(query)
    if not usuario:
        raise HTTPException(404, "Usuario no encontrado")

    return usuario
def login_usuario(correo, password):
    # 🔍 Buscar usuario por correo
    usuario = usuarios.find_one({"correo": correo})

    if not usuario:
        return None

    # 🔐 Verificar contraseña con bcrypt
    if not bcrypt.checkpw(password.encode(), usuario["password"].encode()):
        return None

    # 🚫 Verificar estado (opcional pero recomendable)
    if usuario.get("estado") != "activo":
        raise HTTPException(403, "Usuario inactivo")

    return usuario
