from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "geoluminate.contrib.users"
    label = "users"

    def ready(self):
        from actstream import registry

        from . import receivers  # noqa: F401

        registry.register(self.get_model("User"))
        return super().ready()
