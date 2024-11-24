# Generated by Django 5.1.2 on 2024-11-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mygrace', '0003_remove_mygraceuser_address_remove_mygraceuser_clan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='address',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='clan',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='community',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='family_name',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='lga_of_origin',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='lga_of_residence',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='public_visibility',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='sex',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='state_of_origin',
        ),
        migrations.RemoveField(
            model_name='mygraceadmin',
            name='state_of_residence',
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='clan',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='community',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='family_name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='lga_of_origin',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='lga_of_residence',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='occupation',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/'),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='public_visibility',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='sex',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='state_of_origin',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='mygraceuser',
            name='state_of_residence',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
