import os
from django.db import migrations

class Migration(migrations.Migration):
    # migration to create a default superuser at app startup, using environment variables
    
    dependencies = [
        ('samu', '0001_initial'),
    ]

    def generate_superuser(apps, schema_editor):
        from ..models import User

        username = os.getenv("SUPERUSER_USERNAME", "change-me")
        name = os.getenv("SUPERUSER_NAME", "change-me")
        email = os.getenv("SUPERUSER_EMAIL", "change-me")
        password = os.getenv("SUPERUSER_PASSWORD", "change-me")

        superuser = User.objects.create_superuser(
            name=name,
            username=username,
            email=email,
            password=password
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]