# Generated by Django 5.1.2 on 2024-11-15 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0016_remove_mygraceuser_groups_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='verification',
            name='has_requested_verification',
            field=models.BooleanField(default=False),
        ),
    ]