# Generated by Django 3.2.8 on 2021-10-30 00:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_auto_20211029_1755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(related_name='_network_user_following_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follower',
        ),
    ]
