from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.enums import Choices


class User(AbstractUser):
    pass

class Listing(models.Model):
    ELECTRONICS = 'EL'
    CLOTHING = 'CL'
    FOOD = 'FD'
    HOME = 'HO'
    TOYS = 'TO'
    MISC = 'MS'
    CATEGORIES = [
        (MISC, 'Miscellaneous'),
        (ELECTRONICS, 'Electronics'),
        (CLOTHING, 'Clothing'),
        (FOOD, 'Food'),
        (HOME, 'Home'),
        (TOYS, 'Toys')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    thumbnail = models.CharField(max_length=256, null=True)
    description = models.TextField()
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=2, choices=CATEGORIES, default=MISC)

    def __str__(self):
        return f"{self.owner}:{self.name}:{self.thumbnail}:{self.description}:{self.category}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}:{self.listing.name}${self.price}"


class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)

    def __str__(self):
        return self.text


class Watchlist(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner}:({self.listing})"
