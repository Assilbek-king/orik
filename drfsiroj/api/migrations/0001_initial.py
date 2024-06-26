# Generated by Django 5.0 on 2024-06-30 16:16

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='upload')),
            ],
        ),
        migrations.CreateModel(
            name='Unit2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserSite2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('phone_num', models.CharField(max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('status', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Person2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('phone_num', models.CharField(blank=True, max_length=200)),
                ('reset_password_token', models.CharField(blank=True, max_length=6, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True)),
                ('image1', models.ImageField(upload_to='upload')),
                ('price', models.IntegerField(default=0)),
                ('compound', models.TextField(blank=True)),
                ('storage', models.TextField(blank=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('discount', models.IntegerField(default=0)),
                ('is_new', models.BooleanField(default=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category2')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.unit2')),
            ],
        ),
        migrations.CreateModel(
            name='Cart2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200)),
                ('is_accepted', models.BooleanField(default=False)),
                ('is_payed', models.BooleanField(default=False)),
                ('pr_count', models.IntegerField(default=0)),
                ('total_price', models.IntegerField(default=0)),
                ('order', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('finished_at', models.DateTimeField(default=datetime.datetime.now)),
                ('status', models.IntegerField(default=0)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('siteuser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.usersite2')),
            ],
        ),
    ]
