from pydantic import BaseModel


class TarjetaCreate(BaseModel):
    uid: str

class AsignarTarjeta(BaseModel):
    tarjeta_id: str
    cliente_id: str