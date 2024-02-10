# import json

# from channels.db import database_sync_to_async
# from channels.generic.websocket import AsyncWebsocketConsumer

# from .models import Message, Room


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

#     @database_sync_to_async
#     def create_message(self, message, username, room_name):
#         room = Room.objects.get_or_create(name=room_name)[0]
#         message_obj = Message.objects.create(
#             message=message,
#             username=username,
#             room=room,
#         )
#         return message_obj

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         message = data["message"]
#         username = data["username"]
#         room_name = self.room_name

#         message_obj = await self.create_message(message, username, room_name)
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 "type": "chat.message",
#                 "message": message_obj.message,
#                 "username": message_obj.username,
#                 "timestamp": str(message_obj.timestamp),
#             },
#         )

#     async def chat_message(self, event):
#         message = event["message"]
#         username = event["username"]
#         timestamp = event["timestamp"]

#         await self.send(
#             text_data=json.dumps(
#                 {
#                     "message": message,
#                     "username": username,
#                     "timestamp": timestamp,
#                 }
#             )
#         )
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

import jwt
from django.conf import settings

from account.models import User
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        query_string = self.scope["query_string"].decode("utf-8")
        query_params = parse_qs(query_string)
        auth_token = query_params.get("token", [""])[0]
        user = await self.get_user_from_token(auth_token)
        if user:
            self.user = user
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()


        # await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def create_message(self, message, username, room_name,user):
        room = Room.objects.get_or_create(name=room_name)[0]
        message_obj = Message.objects.create(
            message=message,
            username=username,
            room=room,
            user=user,
        )
        return message_obj

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = data["username"]
        room_name = self.room_name

        message_obj = await self.create_message(message, username, room_name,self.user)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_obj.message,
                "username": message_obj.username,
                "timestamp": str(message_obj.timestamp),
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        timestamp = event["timestamp"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "username": username,
                    "timestamp": timestamp,
                }
            )
        )

    @database_sync_to_async
    def get_user_from_token(self, auth_token):
        try:
            payload = jwt.decode(auth_token, settings.SECRET_KEY, algorithms=["HS256"])
            return User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            return None
        except (jwt.InvalidTokenError, User.DoesNotExist):
            return None
