from pydantic import BaseModel
from typing import Optional

class DeviceTokenSchema(BaseModel):
    token: str
    user_id: Optional[str] = None
    device: Optional[str] = "android"