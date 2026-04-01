from fastapi import FastAPI
from routes.usuario_routes import router as usuario_router
from routes.tarjeta_router import router as tarjeta_router
from routes.recarga_router import router as recarga_router
app = FastAPI()
app.include_router(usuario_router)
app.include_router(tarjeta_router)
app.include_router(recarga_router)



