from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model

class AccountsConfig(AppConfig):
    name = 'accounts_app'

    def ready(self):
        from . import signals