from fastapi import APIRouter
from models.micro import MicroCreate, MicroUpdate
from services.micro_service import (
    crear_micro,
    listar_micros,
    obtener_micro,
    actualizar_micro,
    eliminar_micro,
    asignar_dispositivo,
    quitar_dispositivo
)

router = APIRouter(prefix="/micros", tags=["Micros"])

# CREAR
@router.post("/")
def crear(data: MicroCreate):
    return crear_micro(data)

# LISTAR
@router.get("/")
def listar():
    return listar_micros()

# OBTENER UNO
@router.get("/{micro_id}")
def obtener(micro_id: str):
    return obtener_micro(micro_id)

# ACTUALIZAR
@router.put("/{micro_id}")
def actualizar(micro_id: str, data: MicroUpdate):
    return actualizar_micro(micro_id, data)

# ELIMINAR
@router.delete("/{micro_id}")
def eliminar(micro_id: str):
    return eliminar_micro(micro_id)

# ASIGNAR DISPOSITIVO
@router.post("/{micro_id}/dispositivos/{device_id}")
def asignar_device(micro_id: str, device_id: str):
    return asignar_dispositivo(micro_id, device_id)

# QUITAR DISPOSITIVO
@router.delete("/{micro_id}/dispositivos/{device_id}")
def quitar_device(micro_id: str, device_id: str):
    return quitar_dispositivo(micro_id, device_id)