# Generated by Django 5.1.2 on 2024-11-10 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0007_remove_activitylog_details_alter_activitylog_action_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='activitylog',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='activitylog',
            name='action',
            field=models.CharField(max_length=100),
        ),
    ]
