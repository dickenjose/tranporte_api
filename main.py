from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.usuario_routes import router as usuario_router
from routes.tarjeta_router import router as tarjeta_router
from routes.recarga_router import router as recarga_router
from routes.device_token_routes import router as device_token_router

from config.firebase_config import init_firebase
from routes.notification_routes import router as notification_router
from routes.micro_routes import router as micro_router
from routes.devicer_routes import router as device_router


app = FastAPI()
init_firebase()

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
app.include_router(notification_router)
app.include_router(micro_router)
app.include_router(device_router)