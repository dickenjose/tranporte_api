from pydantic import BaseModel, EmailStr
from typing import Optional


class Perfil(BaseModel):
    tipo_cliente: Optional[str] = None


class UsuarioCreate(BaseModel):
    nombre: str
    ci: str
    telefono: Optional[str] = None
    correo: EmailStr
    password: str
    rol: str = "cliente"
    perfil: Optional[Perfil] = None


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    perfil: Optional[Perfil] = None
    estado: Optional[str] = None