from django.apps import AppConfig


class AndonmesinappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AndonMesinApp'


    def ready(self):
        # Import signals saat aplikasi dimulai
        import AndonMesinApp.routing
