from django.apps import AppConfig


class BoardsConfig(AppConfig):
    name = 'boards_app'

    def ready(self):
        import boards_app.signals
