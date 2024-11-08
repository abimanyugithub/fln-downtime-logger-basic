# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Mesin, Downtime

class MesinDowntimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Menyambungkan WebSocket ke room ini
        self.room_name = 'mesin_downtime_room'
        self.room_group_name = f'room_{self.room_name}'

        # Bergabung ke grup untuk menerima pesan
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Terima koneksi WebSocket
        await self.accept()

        # Kirimkan data mesin dan downtime yang sudah diurutkan setelah koneksi
        await self.send_mesin_and_downtime_data()

    async def disconnect(self, close_code):
        # Keluar dari grup jika WebSocket terputus
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Menerima data dari WebSocket (misalnya perintah atau pesan)
        # Jika ada perintah untuk melakukan update atau mengambil data, kirimkan update
        await self.channel_layer.group_send(
            self.room_group_name,  # Pastikan nama grup sesuai
            {
                'type': 'send_updates',  # Jenis pesan untuk mengirimkan data terbaru
            }
        )

    async def send_updates(self, event):
        # Fungsi ini dipanggil untuk mengirimkan data yang diperbarui ke klien
        await self.send_mesin_and_downtime_data()

    async def send_mesin_and_downtime_data(self):
        # Ambil semua objek Mesin dan urutkan berdasarkan kategori (desc) dan nomor_mesin (asc)
        mesin_data = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

        # Ambil semua objek Downtime dan urutkan berdasarkan start_time (desc)
        downtime_data = Downtime.objects.all().order_by('-start_time')

        # Format data mesin dan downtime menjadi format JSON
        mesin_list = [{"id": mesin.id} for mesin in mesin_data]
        downtime_list = [{"id": downtime.id} for downtime in downtime_data]

        # Kirim data mesin dan downtime ke WebSocket
        await self.send(text_data=json.dumps({
            'mesins': mesin_list,
            'downtimes': downtime_list
        }))
