# Generated by Django 5.1.2 on 2024-11-07 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygraceuser',
            name='sex',
        ),
    ]
