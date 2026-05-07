def usuario_schema(usuario) -> dict:
    return {
        "id": str(usuario["_id"]),
        "nombre": usuario["nombre"],
        "ci": usuario["ci"],
        "correo": usuario["correo"],
        "telefono": usuario.get("telefono"),

        # 🔥 CAMBIO CLAVE
        "roles": usuario.get("roles", ["cliente"]),

        "estado": usuario.get("estado"),
        "perfil": usuario.get("perfil", {})
    }


def usuarios_schema(usuarios) -> list:
    return [usuario_schema(u) for u in usuarios]
