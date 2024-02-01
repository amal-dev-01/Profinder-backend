
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .serializers import NotificationSerializer
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
import jwt
from django.conf import settings
from account.models import User

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode('utf-8')
        # print(query_string,'query_string')
        query_params = parse_qs(query_string)
        # print(query_params,'query_params')
        auth_token = query_params.get('token', [''])[0]
        # print('auth_token',auth_token)
        user = await self.get_user_from_token(auth_token)
        # print(user.id,'lllllllll')

        if user:
            self.user = user
            self.group_name = f"user_{self.user.id}_notifications"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()



    @database_sync_to_async
    def get_user_from_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token,settings.SECRET_KEY, algorithms=['HS256'])
            return User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except (jwt.InvalidTokenError, User.DoesNotExist):
            # Invalid token or user not found
            return None



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

