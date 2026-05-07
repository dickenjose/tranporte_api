from fastapi import APIRouter, HTTPException, status
from schemas.device_token_schema import DeviceTokenSchema
from services.device_token_service import DeviceTokenService

router = APIRouter(prefix="/device-token", tags=["Device Tokens"])

service = DeviceTokenService()


# ✅ Guardar / actualizar token
@router.post("/", status_code=status.HTTP_201_CREATED)
def save_token(data: DeviceTokenSchema):
    try:
        return service.save_token(
            token=data.token,
            user_id=data.user_id,
            device=data.device
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🔍 Obtener tokens por usuario
@router.get("/user/{user_id}")
def get_tokens_by_user(user_id: str):
    try:
        tokens = service.get_tokens_by_user(user_id)
        return {"tokens": tokens}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 🧹 Eliminar token
@router.delete("/{token}")
def delete_token(token: str):
    try:
        return service.delete_token(token)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))