# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Mesin
from asgiref.sync import sync_to_async
from django.core.serializers import serialize

class MesinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomGroupName = "group_data"
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            self.roomGroupName,
            {
                'type': 'send_updates',
            }
        )

    async def send_updates(self, event):
        # Query your MySQL database for updates
        queryset = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')
        data = [{'field1': item.nomor_mesin, 'field2': item.kategori.kategori} for item in queryset]

        # Send the updated data to connected clients
        await self.send(text_data=json.dumps(data))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.roomGroupName , 
            self.channel_name 
        )