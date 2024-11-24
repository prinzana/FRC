# Generated by Django 5.1.2 on 2024-11-07 16:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('mygrace', '0002_remove_mygraceuser_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mygraceuser',
            name='address',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='clan',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='community',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='family_name',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='lga_of_origin',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='lga_of_residence',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='occupation',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='profile_picture',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='public_visibility',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='state_of_origin',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='state_of_residence',
        ),
        migrations.RemoveField(
            model_name='mygraceuser',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='mygraceuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='USER', max_length=50),
        ),
        migrations.AlterField(
            model_name='verification',
            name='id_document',
            field=models.FileField(default='default/path/to/file', upload_to='verification_docs/'),
        ),
        migrations.AlterField(
            model_name='verification',
            name='id_number',
            field=models.CharField(default='default_id_number', max_length=255),
        ),
        migrations.AlterField(
            model_name='verification',
            name='id_type',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AlterField(
            model_name='verification',
            name='submitted_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='verification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MyGraceAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('fullname', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='ADMIN', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('community', models.CharField(blank=True, max_length=255, null=True)),
                ('clan', models.CharField(max_length=255, null=True)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('state_of_residence', models.CharField(max_length=255, null=True)),
                ('lga_of_residence', models.CharField(max_length=255, null=True)),
                ('occupation', models.CharField(max_length=255, null=True)),
                ('sex', models.CharField(max_length=255, null=True)),
                ('state_of_origin', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profiles/')),
                ('public_visibility', models.BooleanField(default=True)),
                ('lga_of_origin', models.CharField(max_length=255, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
