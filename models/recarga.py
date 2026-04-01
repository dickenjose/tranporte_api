from pydantic import BaseModel

class RecargaCreate(BaseModel):
    uid: str
    monto: float
    metodo: str = "efectivo"
