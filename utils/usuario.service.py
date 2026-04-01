def login(correo, password):
    usuario = usuarios.find_one({"correo": correo})
    if not usuario:
        raise HTTPException(400, "Credenciales incorrectas")

    if not verificar_password(password, usuario["password"]):
        raise HTTPException(400, "Credenciales incorrectas")

    token = crear_token({
        "id": str(usuario["_id"]),
        "correo": usuario["correo"],
        "rol": usuario["rol"]
    })

    return {
        "token": token,
        "usuario": {
            "id": str(usuario["_id"]),
            "nombre": usuario["nombre"],
            "correo": usuario["correo"]
        }
    }
