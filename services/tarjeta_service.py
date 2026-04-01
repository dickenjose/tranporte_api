from config.database import db, usuarios
from fastapi import HTTPException
from datetime import datetime
from bson import ObjectId

tarjetas = db.tarjetas


def crear_tarjeta(data):
    if tarjetas.find_one({"uid": data.uid}):
        raise HTTPException(status_code=400, detail="Tarjeta ya existe")

    nueva = {
        "uid": data.uid,
        "cliente_id": None,
        "saldo": 0,
        "estado": "activa",
        "fecha_registro": datetime.utcnow()
    }

    result = tarjetas.insert_one(nueva)
    return str(result.inserted_id)


def listar_tarjetas():
    return tarjetas.find()


def asignar_tarjeta(data):
    tarjeta = tarjetas.find_one({"_id": ObjectId(data.tarjeta_id)})
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    if tarjeta.get("cliente_id"):
        raise HTTPException(status_code=400, detail="Tarjeta ya asignada")

    usuario = usuarios.find_one({"_id": ObjectId(data.cliente_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if usuario.get("rol") != "cliente":
        raise HTTPException(status_code=400, detail="Solo clientes pueden tener tarjeta")

    tarjetas.update_one(
        {"_id": ObjectId(data.tarjeta_id)},
        {"$set": {"cliente_id": ObjectId(data.cliente_id)}}
    )