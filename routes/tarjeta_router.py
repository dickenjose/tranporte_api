from fastapi import APIRouter
from models.tarjeta import TarjetaCreate, AsignarTarjeta
from services.tarjeta_service import crear_tarjeta, listar_tarjetas, asignar_tarjeta
from schemas.tarjeta_schema import tarjetas_schema

router = APIRouter()


@router.post("/tarjetas")
def create_tarjeta(data: TarjetaCreate):
    return {"id": crear_tarjeta(data)}


@router.get("/tarjetas")
def get_tarjetas():
    return tarjetas_schema(listar_tarjetas())


@router.post("/tarjetas/asignar")
def asignar(data: AsignarTarjeta):
    asignar_tarjeta(data)
    return {"mensaje": "Tarjeta asignada correctamente"}