import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from chat.models import Conversation,Message
from account.models import User
from channels.generic.websocket import JsonWebsocketConsumer
from chat.serilalizers import MessageSerializer
 
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class TextRoomConsumer(WebsocketConsumer):
    def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        message_type = text_data_json.get('type', None)
        
        if message_type == 'custom_message':
            content = text_data_json['content']
            sender = text_data_json['sender']

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': content,
                    'sender': sender
                }
            )


    def chat_message(self, event):
        text = event['message']
        sender = event['sender']
        self.send(text_data=json.dumps({
            'text': text,
            'sender': sender
        }))




# from asgiref.sync import async_to_sync
# from channels.generic.websocket import JsonWebsocketConsumer
# from chat.models import Conversation
 
 
# class ChatConsumer(JsonWebsocketConsumer):
#     """
#     This consumer is used to show user's online status,
#     and send notifications.
#     """
 
#     def __init__(self, *args, **kwargs):
#         super().__init__(args, kwargs)
#         self.user = None
#         self.conversation_name = None
#         self.conversation = None


    # def connect(self):
    #     self.user = self.scope["user"]
    #     if not self.user.is_authenticated:
    #         return
    
    #     self.accept()
    #     # self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
    #     # self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)
    
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.conversation_name,
    #         self.channel_name,
    #     )
    
    # def disconnect(self, code):
    #     print("Disconnected!")
    #     return super().disconnect(code)
 
    # def receive_json(self, content, **kwargs):
    #     message_type = content["type"]
    #     if message_type == "chat_message":
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_name,
    #             {
    #                 "type": "chat_message_echo",
    #                 "name": content["name"],
    #                 "message": content["message"],
    #             },
    #         )
    #     return super().receive_json(content, **kwargs)
 
    # def chat_message_echo(self, event):
    #     print(event)
    #     self.send_json(event)