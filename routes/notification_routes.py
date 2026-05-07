from fastapi import APIRouter
from schemas.notification_schema import NotificationSchema
from services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])

service = NotificationService()

@router.post("/send")
def send_notification(data: NotificationSchema):
    return service.send_to_all(
        title=data.title,
        body=data.body,
    )