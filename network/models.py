from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class User(AbstractUser):
    following = models.ManyToManyField("User")

class Post(models.Model):
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User")

    def __str__(self):
        return json.dumps({
            "owner": self.owner.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "likes": list(self.likes.all().values_list('username', flat=True))
        })
