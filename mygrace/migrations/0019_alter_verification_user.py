# Generated by Django 5.1.2 on 2024-11-16 00:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0018_alter_verification_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
