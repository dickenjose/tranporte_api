from fastapi import APIRouter
from models.device import DeviceCreate, DeviceUpdate
from services.device_service import (
    crear_device,
    listar_devices,
    obtener_device,
    actualizar_device,
    eliminar_device,
    asignar_device_micro,
    quitar_device_micro
)

router = APIRouter(prefix="/devices", tags=["Devices"])


# ➕ CREAR
@router.post("/")
def crear(data: DeviceCreate):
    return crear_device(data)


# 📋 LISTAR
@router.get("/")
def listar():
    return listar_devices()


# 🔍 OBTENER
@router.get("/{device_id}")
def obtener(device_id: str):
    return obtener_device(device_id)


# ✏️ ACTUALIZAR
@router.put("/{device_id}")
def actualizar(device_id: str, data: DeviceUpdate):
    return actualizar_device(device_id, data)


# ❌ ELIMINAR
@router.delete("/{device_id}")
def eliminar(device_id: str):
    return eliminar_device(device_id)


# 🔗 ASIGNAR A MICRO
@router.post("/{device_id}/micro/{micro_id}")
def asignar(device_id: str, micro_id: str):
    return asignar_device_micro(device_id, micro_id)


# 🔓 DESASIGNAR
@router.delete("/{device_id}/micro")
def quitar(device_id: str):
    return quitar_device_micro(device_id)