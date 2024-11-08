
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Mesin, Downtime
from django.core.serializers import serialize

class MesinConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        # Menentukan nama room dan group
        self.room_name = 'mesin_room'
        self.room_group_name = f'room_{self.room_name}'

        # Gabungkan ke group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Terima koneksi WebSocket
        await self.accept()
        
        # Kirim data mesin pertama kali
        await self.send_mesin_data()

    # Menerima data dari frontend (misalnya permintaan update)
    async def receive(self, text_data):
        # Anda bisa memproses data yang diterima di sini, misalnya perbarui data mesin
        # Kalau diperlukan, Anda bisa mengambil atau mengubah data berdasarkan 'text_data'
        
        # Kirim event ke group untuk memperbarui semua anggota room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_updates',  # Ini adalah method untuk mengirimkan pembaruan
            }
        )

    # Method untuk mengirimkan pembaruan kepada group
    async def send_updates(self, event):
        # Kirim data mesin terbaru setelah event diterima
        await self.send_mesin_data()

    async def disconnect(self, close_code):
        # Saat koneksi WebSocket ditutup, keluar dari group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Mengambil dan mengirimkan data mesin dari database
    async def send_mesin_data(self):
        # Ambil data mesin, urutkan sesuai kategori dan nomor mesin
        mesin_list = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

        '''# Serialize data mesin ke format JSON
        serialized_data = serialize('json', mesin_data)
        
        # Format data serialized menjadi string JSON yang valid
        serialized_data = serialized_data.replace("model", "type")  # Gantilah "model" dengan "type" agar sesuai standar JSON
        
        # Kirim data ke WebSocket sebagai pesan JSON
        await self.send(text_data=serialized_data)'''
        # Convert data mesin menjadi format yang bisa dikirimkan melalui WebSocket
        mesin_data = []
        for mesin in mesin_list:
            mesin_data.append({
                'id': mesin.id,
                # Sesuaikan dengan field yang ada di model Mesin
            })

        # Kirim data mesin ke WebSocket
        await self.send(text_data=json.dumps({
            'type': 'mesin_list',
            'mesins': mesin_data
        }))