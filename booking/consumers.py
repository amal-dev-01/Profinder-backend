import json
from urllib.parse import parse_qs

import jwt
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

from account.models import User


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        auth_token = query_params.get("token", [""])[0]
        user = await self.get_user_from_token(auth_token)

        if user:
            self.user = user
            self.group_name = f"user_{self.user.id}_notifications"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    @database_sync_to_async
    def get_user_from_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
            return User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except (jwt.InvalidTokenError, User.DoesNotExist):
            # Invalid token or user not found
            return None

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))

    # async def receive(self, text_data):
    #     # text_data_json = json.loads(text_data)
    #     # message = text_data_json['message']
    #     # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json.get('message', '')

    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message_type = text_data_json.get('type', '')

    #     if message_type == 'send_notification':
    #         message = text_data_json.get('message', '')
    #         await self.send(text_data=json.dumps({
    #             'type': 'acknowledge_notification',
    #             'message': 'Notification received successfully',
    #         }))
    #     else:
    #         print(f"Unhandled message type: {message_type}")
