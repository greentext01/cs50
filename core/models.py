from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    division = models.ForeignKey(
        "Division", on_delete=models.PROTECT, null=True, blank=True)


class Division(models.Model):
    name = models.CharField(max_length=64, default="", unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=64)
    color = ColorField(default="#FFFFFF")
    teacher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subject_teacher")

    def __str__(self):
        return self.name


class Period(models.Model):
    day = models.PositiveIntegerField()
    time = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    room = models.PositiveIntegerField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def serialize(self):
        return {
            'day': self.day,
            'time': self.time,
            'duration': self.duration,
            'room': self.room,
            'subject': self.subject_id,
            'division': self.division_id,
            'teacher': self.subject.teacher.username,
            'name': self.subject.name,
            'color': self.subject.color,
            'id': self.pk,
        }

    def __str__(self):
        return self.subject.name


class Assignment(models.Model):
    instructions = models.TextField()
    finished = models.ManyToManyField(User)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due = models.DateTimeField()

    def serialize(self, request):
        return {
            'instructions': self.instructions,
            'due': self.due.isoformat(),
            'finished': request.user in self.finished.all(),
            'subject': self.subject.name,
            'id': self.pk
        }


class Grade(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name="grade_quiz")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='grades')
    grade = models.IntegerField()
    time_solved = models.DateTimeField(auto_now_add=True)
    denominator = models.IntegerField()


class Quiz(models.Model):
    name = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_owner')
    grades = models.ManyToManyField(User, through=Grade)
    division = models.ForeignKey(Division, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    due = models.DateTimeField()

    def serialize(self, request):
        options = [q.serialize() for q in self.textquestion_set.all()] + \
            [q.serialize() for q in self.multiplechoicequestion_set.all()]

        return {
            'name': self.name,
            'owner': self.owner,
            'due': self.due.isoformat(),
            'finished': request.user in self.finished.all(),
            'subject': self.subject.name,
            'id': self.pk,
            'options': options
        }


class TextQuestion(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    content = models.TextField()
    answer = models.TextField()

    def serialize(self):
        return {
            'content': self.content,
            'answer': self.answer
        }


class MultipleChoiceQuestion(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    answer = models.ForeignKey('Option', on_delete=models.CASCADE, null=True)
    title = models.TextField()

    def serialize(self):
        return {
            'answer': self.answer.pk,
            'options': [o.content for o in self.option_set.all()]
        }


class Option(models.Model):
    question = models.ForeignKey(
        'MultipleChoiceQuestion', on_delete=models.CASCADE)
    content = models.TextField()
