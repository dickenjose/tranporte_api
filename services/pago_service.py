from config.database import db
from datetime import datetime, timedelta

# 📦 colecciones
tarjetas = db.tarjetas
tarifas = db.tarifas
transacciones = db.transacciones


def procesar_pago(uid, tipo_tarifa, bus_id):

    # 🔍 buscar tarjeta por UID (solo entrada)
    tarjeta = tarjetas.find_one({"uid": uid})

    if not tarjeta:
        transacciones.insert_one({
            "estado": "error",
            "mensaje": "Tarjeta no registrada",
            "fecha": datetime.utcnow()
        })
        return {"estado": "error", "mensaje": "Tarjeta no registrada"}

    # 🚫 validar estado
    if tarjeta.get("estado") != "activa":
        return {"estado": "error", "mensaje": "Tarjeta bloqueada"}

    # ⏱ 🔥 COOLDOWN (anti doble cobro)
    cooldown_segundos = 3

    ultima = transacciones.find_one(
        {
            "tarjeta_id": tarjeta["_id"],
            "estado": "aprobado"
        },
        sort=[("fecha", -1)]
    )

    if ultima:
        tiempo_actual = datetime.utcnow()
        diferencia = tiempo_actual - ultima["fecha"]

        if diferencia < timedelta(seconds=cooldown_segundos):
            return {
                "estado": "rechazado",
                "mensaje": "Lectura duplicada"
            }

    # 💲 buscar tarifa
    tarifa = tarifas.find_one({
        "tipo": tipo_tarifa,
        "activo": True
    })

    if not tarifa:
        return {"estado": "error", "mensaje": "Tarifa no encontrada"}

    saldo = tarjeta.get("saldo", 0)
    precio = tarifa.get("precio", 0)

    # 💰 comisión sistema (10%)
    comision = round(precio * 0.1, 2)
    monto_chofer = round(precio - comision, 2)

    # ❌ saldo insuficiente
    if saldo < precio:
        transacciones.insert_one({
            "tarjeta_id": tarjeta["_id"],
            "dispositivo_id": bus_id,

            "tipo_tarifa": tipo_tarifa,
            "monto": precio,

            "saldo_antes": saldo,
            "saldo_despues": saldo,

            "estado": "rechazado",
            "mensaje": "Saldo insuficiente",

            "fecha": datetime.utcnow()
        })

        return {"estado": "rechazado", "mensaje": "Saldo insuficiente"}

    # 💸 actualizar saldo de forma segura
    resultado = tarjetas.update_one(
        {
            "_id": tarjeta["_id"],
            "saldo": {"$gte": precio}
        },
        {
            "$inc": {"saldo": -precio}
        }
    )

    if resultado.modified_count == 0:
        return {"estado": "rechazado", "mensaje": "Saldo insuficiente"}

    nuevo_saldo = saldo - precio

    # 🧾 guardar transacción
    transacciones.insert_one({
        "tarjeta_id": tarjeta["_id"],
        "dispositivo_id": bus_id,

        "tipo_tarifa": tipo_tarifa,
        "monto": precio,

        "comision_sistema": comision,
        "monto_chofer": monto_chofer,

        "saldo_antes": saldo,
        "saldo_despues": nuevo_saldo,

        "estado": "aprobado",
        "mensaje": "OK",

        "fecha": datetime.utcnow()
    })

    # 📤 respuesta final (puedes devolver UID sin guardarlo)
    return {
        "estado": "aprobado",
        "saldo": nuevo_saldo,
        "mensaje": "OK",
        "uid": uid
    }
