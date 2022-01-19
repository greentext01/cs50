from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Division(models.Model):
    students = models.ManyToManyField(User)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="division_teacher")


class Subject(models.Model):
    name = models.CharField(max_length=64)
    color = models.IntegerField()
    students = models.ForeignKey(Division, on_delete=models.CASCADE)


class Period(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    duration = models.IntegerField()
