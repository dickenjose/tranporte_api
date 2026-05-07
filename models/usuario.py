from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Perfil(BaseModel):
    tipo_cliente: Optional[str] = None


class UsuarioCreate(BaseModel):
    nombre: str
    ci: str
    telefono: Optional[str] = None
    correo: EmailStr
    password: str

    # 🔥 CAMBIO AQUÍ
    roles: Optional[List[str]] = ["cliente"]

    perfil: Optional[Perfil] = None


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None

    # 🔥 CAMBIO AQUÍ
    roles: Optional[List[str]] = None

    perfil: Optional[Perfil] = None
    estado: Optional[str] = None
