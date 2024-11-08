# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Mesin

class MesinConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'mesin_room'
        self.room_group_name = f"mesin_{self.room_name}"

        # Bergabung ke group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Kirimkan data mesin dan downtime yang sudah diurutkan setelah koneksi
        await self.send_mesin_data()

    async def disconnect(self, close_code):
        # Tinggalkan group ketika WebSocket terputus
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def send_mesin_data(self):
        queryset = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

        # Ubah queryset menjadi list of dictionaries
        data = [
            {
                'nomor_mesin': mesin.nomor_mesin,
                'kategori': mesin.kategori.kategori,
                'status': mesin.status,
            }
            for mesin in queryset
        ]

        # Send the updated data to connected clients
        await self.send(text_data=json.dumps(data))

    # Terima pesan dari grup (untuk pembaruan atau penghapusan)
    async def update_mesin(self, event):
        # Kirim pesan ke WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
   