# Generated by Django 5.1.2 on 2024-11-23 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0030_remove_facedescriptor_converted_face_descriptor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facedescriptor',
            name='numpy_face_descriptor',
        ),
    ]
