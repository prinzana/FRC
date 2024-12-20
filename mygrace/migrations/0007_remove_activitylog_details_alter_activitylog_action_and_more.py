# Generated by Django 5.1.2 on 2024-11-10 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0006_activitylog_details_alter_activitylog_action_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='details',
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=models.CharField(choices=[('LOGIN', 'Login'), ('UPDATE', 'Profile Update'), ('PASSWORD_CHANGE', 'Password Change'), ('PROFILE_UPDATE', 'Profile Update'), ('VIEW_PROFILE', 'Profile View')], max_length=50),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
