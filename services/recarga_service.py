from config.database import db
from datetime import datetime
from pymongo import ReturnDocument

# 📦 colecciones
tarjetas = db.tarjetas
recargas = db.recargas


def recargar_saldo(uid, monto, usuario_id, metodo="efectivo", tx_id=None):
    """
    💰 Recarga saldo a una tarjeta

    tx_id: identificador único de transacción (anti-duplicados)
    """

    # 🔒 VALIDACIONES
    if monto <= 0:
        raise ValueError("Monto inválido")

    if metodo not in ["efectivo", "qr", "transferencia"]:
        raise ValueError("Método de pago inválido")

    # 🔁 CONTROL DE DUPLICADOS
    if tx_id:
        existe = recargas.find_one({"tx_id": tx_id})
        if existe:
            return {
                "estado": "ok",
                "mensaje": "Transacción ya procesada",
                "saldo": existe["saldo_despues"]
            }

    # 🔍 BUSCAR TARJETA
    tarjeta = tarjetas.find_one({"uid": uid})

    if not tarjeta:
        raise ValueError("Tarjeta no encontrada")

    if tarjeta.get("estado") != "activa":
        raise ValueError("Tarjeta no activa")

    saldo_actual = tarjeta.get("saldo", 0)

    # 🔥 OPERACIÓN ATÓMICA (CLAVE)
    tarjeta_actualizada = tarjetas.find_one_and_update(
        {"_id": tarjeta["_id"]},
        {"$inc": {"saldo": monto}},
        return_document=ReturnDocument.AFTER
    )

    nuevo_saldo = tarjeta_actualizada["saldo"]

    # 🧾 REGISTRO DE RECARGA
    recarga_doc = {
        "uid": uid,
        "tarjeta_id": tarjeta["_id"],
        "cliente_id": tarjeta.get("cliente_id"),

        "usuario_recarga_id": usuario_id,

        "monto": monto,
        "metodo": metodo,

        "saldo_antes": saldo_actual,
        "saldo_despues": nuevo_saldo,

        "fecha": datetime.utcnow()
    }

    if tx_id:
        recarga_doc["tx_id"] = tx_id

    recargas.insert_one(recarga_doc)

    # 📤 RESPUESTA
    return {
        "estado": "ok",
        "mensaje": "Recarga exitosa",
        "saldo": nuevo_saldo
    }
