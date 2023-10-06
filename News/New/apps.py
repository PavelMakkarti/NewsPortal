from django.apps import AppConfig

class NewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'New'



class NewConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'New'

    def ready(self):
        from . import signals
