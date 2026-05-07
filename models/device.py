from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 🔹 DEVICE (modelo de respuesta completo)
class Device(BaseModel):
    id: str

    # 🔥 identificador físico del ESP32 / lector RFID
    device_id: str

    # 🔗 relación con micro (vehículo)
    micro_id: Optional[str] = None

    # 📡 topic MQTT base (se puede generar en backend)
    topic: Optional[str] = None

    # estado del dispositivo
    estado: str = "activo"

    # control de fechas
    fecha_registro: datetime
    ultima_conexion: Optional[datetime] = None

    # información técnica opcional
    firmware_version: Optional[str] = None
    wifi_ssid: Optional[str] = None


# 🔹 DEVICE CREATE (crear dispositivo)
class DeviceCreate(BaseModel):
    device_id: str
    micro_id: Optional[str] = None
    firmware_version: Optional[str] = None
    wifi_ssid: Optional[str] = None
    estado: Optional[str] = "activo"


# 🔹 DEVICE UPDATE (actualizar dispositivo)
class DeviceUpdate(BaseModel):
    micro_id: Optional[str] = None
    estado: Optional[str] = None
    firmware_version: Optional[str] = None
    wifi_ssid: Optional[str] = None