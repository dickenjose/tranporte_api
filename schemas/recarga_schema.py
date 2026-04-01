def recarga_schema(recarga):
    return {
        "uid": recarga["uid"],
        "monto": recarga["monto"],
        "metodo": recarga["metodo"],
        "saldo_antes": recarga["saldo_antes"],
        "saldo_despues": recarga["saldo_despues"],
        "fecha": recarga["fecha"]
    }


def recargas_schema(recargas):
    return [recarga_schema(r) for r in recargas]
