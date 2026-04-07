from django.apps import AppConfig


class CensesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'censesapp'
    
    def ready(self):
        import censesapp.signals