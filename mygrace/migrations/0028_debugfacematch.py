# Generated by Django 5.1.2 on 2024-11-23 04:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0027_facedescriptor_converted_face_descriptor'),
    ]

    operations = [
        migrations.CreateModel(
            name='DebugFaceMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_descriptor', models.JSONField()),
                ('stored_descriptor', models.JSONField()),
                ('similarity_score', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debug_face_matches', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
