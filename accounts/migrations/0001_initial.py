# Generated by Django 4.0.1 on 2022-01-23 05:06

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=24, unique=True)),
                ('title', models.CharField(max_length=24)),
                ('banner', models.ImageField(upload_to=accounts.models.blog_media_uploader)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11)),
                ('ban', models.BooleanField(default=False)),
                ('access', models.BooleanField(default=False)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField()),
                ('modified_date', models.DateTimeField()),
                ('title', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to=accounts.models.media_uploader)),
                ('body', models.TextField()),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.blog')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.profile'),
        ),
    ]
