import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class NotifyConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "notify"

        # # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        # Send message to room groups
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "notify.message", "message": "reload"}
        )

    # Receive message from room group
    def notify_message(self, event):
        # Send message to WebSocket
        self.send('reload')