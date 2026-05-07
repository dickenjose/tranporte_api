from config.database import usuarios
from fastapi import HTTPException
from bson import ObjectId
import bcrypt
from datetime import datetime


def crear_usuario(data):
    # 🔍 validar correo único
    if usuarios.find_one({"correo": data.correo}):
        raise HTTPException(400, "Correo ya existe")

    # 🔐 hash password
    password_hash = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    # 🎯 manejar roles (nuevo + compatibilidad)
    roles = []
    if hasattr(data, "roles") and data.roles:
        roles = data.roles
    elif hasattr(data, "rol") and data.rol:
        roles = [data.rol]
    else:
        roles = ["cliente"]  # default

    nuevo = {
        "nombre": data.nombre,
        "ci": data.ci,
        "telefono": data.telefono,
        "correo": data.correo,
        "password": password_hash,

        "roles": roles,  # 🔥 cambio principal

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

    # 🔄 compatibilidad con datos antiguos
    if "roles" not in usuario:
        usuario["roles"] = [usuario.get("rol", "cliente")]

    return usuario


def actualizar_usuario(usuario_id, data):
    usuario = obtener_usuario(usuario_id)

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    # 🔐 actualizar password
    if "password" in update_data:
        update_data["password"] = bcrypt.hashpw(
            update_data["password"].encode(), bcrypt.gensalt()
        ).decode()

    # 📧 validar correo único
    if "correo" in update_data and update_data["correo"] != usuario["correo"]:
        if usuarios.find_one({"correo": update_data["correo"]}):
            raise HTTPException(400, "Correo ya existe")

    # 🆔 validar CI único
    if "ci" in update_data and update_data["ci"] != usuario["ci"]:
        if usuarios.find_one({"ci": update_data["ci"]}):
            raise HTTPException(400, "CI ya existe")

    # 🎯 manejar roles correctamente
    if "roles" in update_data:
        if not isinstance(update_data["roles"], list):
            update_data["roles"] = [update_data["roles"]]

    # 🔄 si viene rol antiguo, convertir
    if "rol" in update_data:
        update_data["roles"] = [update_data["rol"]]
        del update_data["rol"]

    usuarios.update_one(
        {"_id": ObjectId(usuario_id)},
        {"$set": update_data}
    )


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

    # 🔄 compatibilidad roles
    if "roles" not in usuario:
        usuario["roles"] = [usuario.get("rol", "cliente")]

    return usuario


def login_usuario(correo, password):
    # 🔍 buscar usuario
    usuario = usuarios.find_one({"correo": correo})

    if not usuario:
        return None

    # 🔐 validar password
    if not bcrypt.checkpw(password.encode(), usuario["password"].encode()):
        return None

    # 🚫 estado
    if usuario.get("estado") != "activo":
        raise HTTPException(403, "Usuario inactivo")

    # 🔄 asegurar roles
    if "roles" not in usuario:
        usuario["roles"] = [usuario.get("rol", "cliente")]

    return usuario
