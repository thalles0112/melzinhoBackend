import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        #print('\033[32m method receive, arg:\033[m',text_data)
        text_data_json = json.loads(text_data)
        text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", 
                                   "id": text_data_json['id'],
                                   "author": text_data_json['author'],
                                   "message": text_data_json['message'],
                                   "command": text_data_json['command'],
                                   "receiver": text_data_json['receiver'],
                                   "timestamp": text_data_json['timestamp'],
                                   }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        #print('\033[32m method chat_message, arg:\033[m ',event)
        # Send message to WebSocket
        self.send(text_data=json.dumps(event))