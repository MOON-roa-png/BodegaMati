from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

class Command(BaseCommand):
    help = "Crea o actualiza un superusuario desde variables de entorno."

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = config("DJANGO_SUPERUSER_USERNAME", default=None)
        email = config("DJANGO_SUPERUSER_EMAIL", default="")
        password = config("DJANGO_SUPERUSER_PASSWORD", default=None)

        if not username or not password:
            self.stdout.write(self.style.WARNING("DJANGO_SUPERUSER_* no seteadas. Omitiendo."))
            return

        obj, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )
        obj.is_staff = True
        obj.is_superuser = True
        obj.email = email or obj.email
        obj.set_password(password)
        obj.save()

        msg = f"Superusuario '{username}' {'creado' if created else 'actualizado'}."
        self.stdout.write(self.style.SUCCESS(msg))
