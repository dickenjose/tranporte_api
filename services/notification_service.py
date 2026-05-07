from firebase_admin import messaging
from config.database import device_tokens

class NotificationService:

    def send_to_all(self, title: str, body: str):
        tokens = [t["token"] for t in device_tokens.find()]

        if not tokens:
            return {"msg": "No hay tokens"}

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=tokens,
        )

        response = messaging.send_each_for_multicast(message)

        return {
            "success": response.success_count,
            "fail": response.failure_count,
        }