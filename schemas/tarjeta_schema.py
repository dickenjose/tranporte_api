def tarjeta_schema(tarjeta) -> dict:
    return {
        "id": str(tarjeta["_id"]),
        "uid": tarjeta.get("uid"),
        "cliente_id": str(tarjeta.get("cliente_id")) if tarjeta.get("cliente_id") else None,
        "saldo": tarjeta.get("saldo"),
        "estado": tarjeta.get("estado"),
        "fecha_registro": tarjeta.get("fecha_registro")
    }


def tarjetas_schema(tarjetas) -> list:
    return [tarjeta_schema(t) for t in tarjetas]