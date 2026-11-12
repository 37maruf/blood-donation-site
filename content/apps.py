from django.apps import AppConfig
from django.db.models.signals import post_migrate


def _seed(sender, **kwargs):
    from .seed import seed_all

    seed_all()


class ContentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "content"

    def ready(self):
        # Runs after every migrate (idempotent). `content` is the last app with models,
        # so permissions of all other apps already exist when groups are built.
        post_migrate.connect(_seed, sender=self, dispatch_uid="content.seed_all")
