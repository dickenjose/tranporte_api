from datetime import datetime
from config.database import device_tokens

class DeviceTokenService:

    def save_token(self, token: str, user_id: str = None, device: str = "android"):

        existing = device_tokens.find_one({"token": token})

        if existing:
            device_tokens.update_one(
                {"token": token},
                {
                    "$set": {
                        "user_id": user_id,
                        "device": device,
                        "updated_at": datetime.utcnow()
                    }
                }
            )
            return {"msg": "Token actualizado"}

        device_tokens.insert_one({
            "token": token,
            "user_id": user_id,
            "device": device,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })

        return {"msg": "Token guardado"}