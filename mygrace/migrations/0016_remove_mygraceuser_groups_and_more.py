# Generated by Django 5.1.2 on 2024-11-13 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0015_alter_mygraceadmin_groups_alter_mygraceadmin_role_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygraceuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='mygraceadmin',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='ADMIN', max_length=10),
        ),
    ]