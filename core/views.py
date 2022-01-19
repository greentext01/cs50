import csv
from io import StringIO
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import BadRequest, PermissionDenied
from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
import json
from django.utils import timezone
from django.utils import dateparse

from core.models import Division, Grade, Period, Subject, User, Assignment, TextQuestion, MultipleChoiceQuestion, Option, Quiz


class CreateSubject(forms.Form):
    name = forms.CharField(max_length=64)
    color = forms.TextInput(attrs={
        'type': 'color'
    })


class CreatePeriod(forms.Form):
    day = forms.IntegerField(max_value=7, min_value=1)
    time = forms.IntegerField(max_value=6, min_value=0)
    room = forms.IntegerField(min_value=0)
    duration = forms.IntegerField(max_value=7, min_value=1)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    division = forms.ModelChoiceField(queryset=Division.objects.all())


class CreateHomework(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ['finished']

        widgets = {
            'due': forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class QuizForm(forms.Form):
    def __init__(self, quiz, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for question in quiz.textquestion_set.all():
            self.fields[f'text_{question.pk}'] = forms.CharField(
                label=question.content)

        for question in quiz.multiplechoicequestion_set.all():
            self.fields[f'multi_{question.pk}'] = forms.ChoiceField(choices=((choice.pk, choice.content) for choice in question.option_set.all()),
                                                                    widget=forms.RadioSelect, label=question.title)

    def get_score(self, quiz):
        try:
            question_count = len(self.fields)
            score = question_count
            for key, value in self.cleaned_data.items():
                if key.startswith('text_'):
                    question = quiz.textquestion_set.get(pk=key.strip('text_'))
                    if question.answer != value:
                        score -= 1
                elif key.startswith('multi_'):
                    question = quiz.multiplechoicequestion_set.get(
                        pk=key.strip('multi_'))
                    
                    if question.answer.pk != int(value):
                        score -= 1

            return score, question_count
        except:
            raise BadRequest


@login_required
def index(request):
    if request.user.groups.filter(name="Teacher").exists():
        quizzes = Quiz.objects.filter(
            subject__teacher=request.user, due__gte=timezone.now() - timezone.timedelta(10)).exclude(
                grades__in=request.user.grades.all().values_list('id')).order_by('-due')

        grades = Grade.objects.filter(quiz__subject__teacher=request.user).order_by('-time_solved')
    else:
        quizzes = Quiz.objects.filter(
            division=request.user.division, due__gte=timezone.now() - timezone.timedelta(10)).exclude(grades__username=request.user).order_by('-due')
        grades = Grade.objects.filter(user=request.user).order_by('-time_solved')

    return render(request, 'index.html', {
        'quizzes': quizzes,
        'grades': grades
    })


def create_accounts(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            data = request.POST.get('csv')
            if data:
                blob = StringIO(data)
                reader = csv.DictReader(blob)
                for row in reader:
                    try:
                        User.objects.create_user(
                            row['username'],
                            row['email'],
                            row['password'],
                            division=Division.objects.get(name=row['division']))
                    except:
                        continue

                    return HttpResponse('Saved!')
            else:
                raise BadRequest
        elif request.method == 'GET':
            return render(request, 'create_accounts.html')
    else:
        raise PermissionDenied


@login_required
def teacher_dash(request):
    if request.user.groups.filter(name='Teacher').exists():
        return render(request, "teacher.html", {
            "form": CreatePeriod(),
            "hwform": CreateHomework(),
            "teacher": "true"
        })
    else:
        raise PermissionDenied()


@login_required
def create_period(request):
    if request.user.groups.filter(name='Teacher').exists():
        form = CreatePeriod(request.POST)
        if form.is_valid():
            period = Period(day=form.cleaned_data["day"], time=form.cleaned_data["time"],
                            duration=form.cleaned_data["duration"], subject=form.cleaned_data["subject"],
                            room=form.cleaned_data["room"], division=form.cleaned_data["division"])

            period.save()
            print(form.cleaned_data["subject"])

            return redirect("teacher")
        else:
            raise BadRequest()
    else:
        raise PermissionDenied()


@login_required
def quiz(request, id):
    quiz = get_object_or_404(Quiz, pk=id)
    if request.user.division == quiz.division and not \
            Grade.objects.filter(user=request.user, quiz=quiz).exists() and not request.user.groups.filter(name='Teacher').exists():

        if request.method == 'GET':
            return render(request, 'quiz.html', {
                'name': quiz.name,
                'form': QuizForm(quiz),
                'id': id,
            })
        elif request.method == 'POST':
            form = QuizForm(quiz, request.POST)
            if form.is_valid():
                grade, denom = form.get_score(quiz)

                grade_model = Grade(quiz=quiz, user=request.user,
                                    grade=grade, denominator=denom)

                grade_model.save()
                return redirect('index')
    else:
        raise PermissionDenied


@login_required
def create_homework(request):
    if request.user.groups.filter(name='Teacher').exists():
        form = CreateHomework(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data["subject"])

            return redirect("teacher")
        else:
            raise BadRequest
    else:
        raise PermissionDenied


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# API routes
@login_required
@require_GET
def get_periods(request, day):
    if request.user.groups.filter(name="Teacher").exists():
        return JsonResponse([item.serialize() for item in Period.objects.filter(subject__teacher=request.user, day=day)], safe=False)
    else:
        return JsonResponse([item.serialize() for item in Period.objects.filter(division=request.user.division, day=day)], safe=False)


@login_required
def delete_period(request, id):
    try:
        Period.objects.get(pk=id).delete()
    except KeyError:
        raise BadRequest
    return HttpResponse()


@login_required
@require_GET
def get_assignments(request):
    if request.user.groups.filter(name="Teacher").exists():
        assignments = [item.serialize(request) for item in Assignment.objects.filter(
            subject__teacher=request.user, due__gte=timezone.now() - timezone.timedelta(10)).order_by('-due')]
    else:
        assignments = [item.serialize(request) for item in Assignment.objects.filter(
            division=request.user.division, due__gte=timezone.now() - timezone.timedelta(10)).order_by('-due')]

    return JsonResponse(assignments, safe=False)


@login_required
@require_POST
def set_finished(request):
    body = json.loads(request.body)

    if body['finished']:
        get_object_or_404(
            Assignment, pk=body['assignment']).finished.add(request.user)
    else:
        get_object_or_404(
            Assignment, pk=body['assignment']).finished.remove(request.user)

    return HttpResponse()


@login_required
def get_subjects(request):
    if request.user.groups.filter(name="Teacher").exists():
        return JsonResponse([{'name': d.name, 'key': d.pk} for d in request.user.subject_teacher.all()], safe=False)

    raise PermissionDenied


@login_required
def get_divisions(request):
    if request.user.groups.filter(name="Teacher").exists():
        return JsonResponse([{'name': d.name, 'key': d.pk} for d in Division.objects.all()], safe=False)

    raise PermissionDenied


@login_required
@require_POST
def new_quiz(request):
    if request.user.groups.filter(name="Teacher").exists():
        data = json.loads(request.body)

        if not data['title']:
            return HttpResponseBadRequest('Quiz does not have a title.')

        if not data['questions']:
            return HttpResponseBadRequest('Quiz does not have any questions.')

        if not data['subject']:
            return HttpResponseBadRequest('Please select a subject for this quiz.')

        if not data['division']:
            return HttpResponseBadRequest('Please select a division to assign this quiz to.')

        if not data['due']:
            return HttpResponseBadRequest('Please select a due date.')

        duedate = dateparse.parse_datetime(data['due'])
        if duedate < timezone.now():
            return HttpResponseBadRequest('Please select a valid due date.')

        for index, question in enumerate(data['questions']):
            if not question['title']:
                return HttpResponseBadRequest(f'Question {index + 1} does not have a title.')
            elif question['answer'] == -1 or question['answer'] == '':
                return HttpResponseBadRequest(f'Question {index + 1} does not have an answer.')

            if question['type'] == 'multi':
                if not question['options']:
                    return HttpResponseBadRequest(f'Question {index + 1} does not have any options.')

                for option_index, option in enumerate(question['options']):
                    if not option:
                        return HttpResponseBadRequest(f'Question {index + 1}, Option {option_index} does not have an answer.')

        quiz = Quiz(name=data['title'], owner=request.user, due=duedate,
                    subject=Subject.objects.get(pk=data['subject']),
                    division=Division.objects.get(pk=data['division']))
        quiz.save()

        for question in data['questions']:
            if question['type'] == 'text':
                question_model = quiz.textquestion_set.create(
                    content=question['title'], answer=question['answer'])
                question_model.save()
            elif question['type'] == 'multi':
                question_model = quiz.multiplechoicequestion_set.create(
                    title=question['title'])
                question_model.save()

                for index, option in enumerate(question['options']):
                    option_model = question_model.option_set.create(content=option)
                    if question['answer'] == index:
                        question_model.answer = option_model
                        question_model.save()

        return HttpResponse()
    else:
        raise PermissionDenied
