from datetime import datetime

def device_token_model(data):
    return {
        "user_id": data.get("user_id"),
        "token": data.get("token"),
        "device": data.get("device", "android"),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }