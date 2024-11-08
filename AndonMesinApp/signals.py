from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Mesin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Sinyal yang akan dipicu setiap kali objek Mesin disimpan (create/update)
@receiver(post_save, sender=Mesin)
def mesin_updated(sender, instance, created, **kwargs):
    # Pastikan hanya saat update (bukan saat pembuatan baru)
    if not created:
        channel_layer = get_channel_layer()
        message = {
            'type': 'mesin_mesin_room',
            'message': f'UserProfile for {instance.nomor_mesin} updated!'
        }

        # Kirimkan pesan ke group WebSocket
        channel_layer.group_send(
            'mesin_mesin_room',  # Nama group yang digunakan pada consumer
            message
        )