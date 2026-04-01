from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from config.database import db

from models.recarga import RecargaCreate
from services.recarga_service import recargar_saldo
from schemas.recarga_schema import recargas_schema

from auth.dependencies import get_current_user

router = APIRouter(prefix="/recargas", tags=["Recargas"])


# 💰 CREAR RECARGA
@router.post("/")
def crear_recarga(data: RecargaCreate, user=Depends(get_current_user)):
    
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")

    # 🔒 VALIDACIONES
    if not data.uid:
        raise HTTPException(status_code=400, detail="UID requerido")

    if data.monto <= 0:
        raise HTTPException(status_code=400, detail="Monto inválido")

    try:
        resultado = recargar_saldo(
            data.uid,
            data.monto,
            str(user["_id"]),
            data.metodo
        )

        return {
            "ok": True,
            "mensaje": "Recarga realizada correctamente",
            "fecha": datetime.utcnow(),
            "data": resultado
        }

    except ValueError as e:
        # errores controlados (ej: saldo inválido)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception:
        # error interno real
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# 📊 LISTAR TODAS LAS RECARGAS
@router.get("/")
def listar_recargas():
    try:
        data = list(db.recargas.find().sort("fecha", -1))

        return {
            "total": len(data),
            "data": recargas_schema(data)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener recargas")


# 👤 RECARGAS POR USUARIO
@router.get("/usuario/{usuario_id}")
def recargas_por_usuario(usuario_id: str):
    try:
        data = list(
            db.recargas.find(
                {"usuario_recarga_id": usuario_id}
            ).sort("fecha", -1)
        )

        return {
            "total": len(data),
            "data": recargas_schema(data)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener recargas")


# 💳 RECARGAS POR TARJETA
@router.get("/tarjeta/{uid}")
def recargas_por_tarjeta(uid: str):
    try:
        data = list(
            db.recargas.find(
                {"uid": uid}
            ).sort("fecha", -1)
        )

        return {
            "total": len(data),
            "data": recargas_schema(data)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener recargas")
