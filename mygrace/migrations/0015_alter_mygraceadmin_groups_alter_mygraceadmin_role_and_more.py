# Generated by Django 5.1.2 on 2024-11-13 04:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('mygrace', '0014_rename_addresses_mygraceuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mygraceadmin',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='mygraceadmin',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin')], default='ADMIN', max_length=10),
        ),
        migrations.AlterField(
            model_name='mygraceadmin',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mygrace.mygraceuser'),
        ),
    ]