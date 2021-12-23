import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import SuspiciousOperation
from django.db import IntegrityError
from django.forms.widgets import Textarea
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseNotAllowed, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage

from network.models import User, Post


class PostForm(forms.Form):
    content = forms.CharField(widget=Textarea)


def render_list(posts, template, request, options={}):
    page = int(request.GET.get("p")) if request.GET.get("p") else 1
    pages = Paginator(posts, 10)

    try:
        return render(request, template, {
            "posts": pages.page(page).object_list,
            "page": page,
            "page_obj": pages.page(page),
        } | options)
    except EmptyPage:
        return HttpResponseRedirect(reverse("index"))

    except PageNotAnInteger :
        return HttpResponseNotFound()


def index(request):
    return render_list(Post.objects.all().order_by("-timestamp"), "network/index.html", request)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post(
                content=form.cleaned_data["content"], owner=request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return SuspiciousOperation()
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required
@require_POST
def edit(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.user == post.owner:
        post.content = json.loads(request.body)["content"]
        post.save()
        return HttpResponse()
    else:
        return HttpResponseNotAllowed()


@login_required
@require_http_methods(["PUT"])
def follow(request, uname):
    data = json.loads(request.body)
    if data.get("follow"):
        request.user.following.add(get_object_or_404(User, username=uname))
    else:
        request.user.following.remove(
            get_object_or_404(User, username=uname))
    return HttpResponse()


def profile(request, uname):
    profile = User.objects.get(username=uname)
    return render_list(Post.objects.filter(owner__username=uname).order_by("-timestamp"), "network/profile.html", request, {
        "profile": profile,
        "followers": User.objects.filter(following=profile),
        "following": profile.following.all(),
    })


@login_required
@require_http_methods(["PUT"])
def like(request, id):
    data = json.loads(request.body)
    post = get_object_or_404(Post, pk=id)
    if data.get("like"):
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    return HttpResponse()


@require_GET
def get_likes(request, id):
    post = get_object_or_404(Post, pk=id)
    return HttpResponse(post.likes.count())
    


@login_required
def following(request):
    return render_list(Post.objects.filter(owner__in=request.user.following.all()).order_by("-timestamp"), "network/following.html", request)
