# Generated by Django 5.1.2 on 2024-11-16 00:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0017_verification_has_requested_verification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
