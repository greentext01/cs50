# Generated by Django 3.2.8 on 2021-10-30 02:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20211029_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='_network_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
