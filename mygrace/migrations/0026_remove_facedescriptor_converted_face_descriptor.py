# Generated by Django 5.1.2 on 2024-11-22 06:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0025_facedescriptor_converted_face_descriptor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facedescriptor',
            name='converted_face_descriptor',
        ),
    ]
