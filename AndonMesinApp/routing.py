from django.urls import re_path
from . import consumers  # Mengimpor consumers.py yang sudah kita buat

# URL pattern untuk WebSocket
websocket_urlpatterns = [
    re_path('ws/mesin/', consumers.MesinConsumer.as_asgi()),  # Menghubungkan URL WebSocket ke consumer
]