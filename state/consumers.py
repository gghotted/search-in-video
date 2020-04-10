from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.video_id = self.scope['url_route']['kwargs']['id']
        self.state_group_name = 'state_%s' % self.video_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.state_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.state_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.state_group_name,
            {
                'type': 'state_message',
                'message': message
            }
        )

    # Receive message from room group
    def state_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))


def announce(channel_name, message):
    channel_layer=get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        channel_name, {
            "type": 'state_message',
            "message": message,
        }
    )