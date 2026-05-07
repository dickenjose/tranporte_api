from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class Micro(BaseModel):
    id: str
    nombre: str
    placa: str

    chofer_id: Optional[str] = None
    chofer_nombre: Optional[str] = None

    linea: Optional[str] = None

    dispositivos: List[str] = Field(default_factory=list)

    estado: str = "activo"

    fecha_registro: datetime
    fecha_actualizacion: Optional[datetime] = None


class MicroCreate(BaseModel):
    nombre: str
    placa: str

    chofer_id: Optional[str] = None
    linea: Optional[str] = None

    estado: Optional[str] = "activo"


class MicroUpdate(BaseModel):
    nombre: Optional[str] = None
    placa: Optional[str] = None

    chofer_id: Optional[str] = None
    linea: Optional[str] = None

    estado: Optional[str] = None