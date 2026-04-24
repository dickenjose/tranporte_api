from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.usuario_routes import router as usuario_router
from routes.tarjeta_router import router as tarjeta_router
from routes.recarga_router import router as recarga_router
from routes.device_token_routes import router as device_token_router


app = FastAPI()

# 🔥 AQUÍ VA CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 👈 permite todos (solo desarrollo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👇 luego tus rutas
app.include_router(usuario_router)
app.include_router(tarjeta_router)
app.include_router(recarga_router)
app.include_router(device_token_router)