# Generated by Django 5.1.2 on 2024-11-12 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0009_alter_verification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygraceuser',
            name='role',
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='clan',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='community',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='family_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='lga_of_origin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='sex',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
