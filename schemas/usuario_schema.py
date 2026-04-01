def usuario_schema(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        "nombre": usuario["nombre"],
        "ci": usuario["ci"],
        "correo": usuario["correo"],
        "telefono": usuario.get("telefono"),
        "rol": usuario.get("rol"),
        "estado": usuario.get("estado"),
        "perfil": usuario.get("perfil", {})  # 🔥 ESTA LÍNEA FALTABA
        
    }


def usuarios_schema(usuarios) -> list:
    return [usuario_schema(u) for u in usuarios]
