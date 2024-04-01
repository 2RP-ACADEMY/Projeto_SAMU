import os
from django.db import migrations
from ..models.requestStatusModel import RequestStatus

class Migration(migrations.Migration):
    dependencies = [
        ('samu', '0002_createsuperuser'),
    ]

    def generate_request_status(apps, schema_editor):
        RequestStatus.objects.create(name="in_progress")
        RequestStatus.objects.create(name="success")
        RequestStatus.objects.create(name="failed")

    operations = [
        migrations.RunPython(generate_request_status),
    ]