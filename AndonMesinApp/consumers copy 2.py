
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Mesin, Downtime
from django.core.serializers import serialize

class TestConsumers(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = 'mesin_room'
        self.room_group_name = f'room_{self.room_name}'

        # Gabungkan ke group mesin
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Terima koneksi WebSocket
        await self.accept()

        # Kirim data mesin saat koneksi dimulai
        '''mesin_data = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')
        data = serialize('json', mesin_data)
        await self.send(text_data=json.dumps({
            'type': 'mesin_data',
            'data': data
        }))'''

        # data = [{'field1': item.id} for item in mesin_data]

        # Send the updated data to connected clients
        # await self.send(text_data=json.dumps(data))

         # Mengirimkan data mesin secara asinkron setelah WebSocket terhubung
        await self.send_mesin_data()
        
    # Menerima data dari frontend jika ada aksi tertentu
    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_updates',
            }
        )

    async def send_updates(self, event):
        # Query your MySQL database for updates
        mesin_data = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')  # Fetch the latest data from your model
        data = serialize('json', mesin_data)
        await self.send(text_data=json.dumps({
            'type': 'mesin_data',
            'data': data
        }))

        # data = [{'field1': item.id} for item in mesin_data]

        # Send the updated data to connected clients
        await self.send(text_data=json.dumps(data))


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name , 
            self.channel_name 
        )

    async def send_mesin_data(self):
        # Ambil data mesin dari database dan urutkan berdasarkan kategori dan nomor mesin
        mesin_data = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

        # Mengonversi queryset Mesin ke format JSON
        # Anda bisa menggunakan serialize untuk serialisasi yang lebih baik
        serialized_data = serialize('json', mesin_data)

        # Kirimkan data mesin dalam format JSON ke client
        await self.send(text_data=serialized_data)

        '''mesin_data = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')
        data = serialize('json', mesin_data)
        await self.send(text_data=json.dumps({
            'type': 'mesin_data',
            'data': data
        }))'''