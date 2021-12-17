from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import IntegrityError
from django.forms.fields import CharField, ChoiceField, IntegerField
from django.forms.widgets import Textarea
from django.http import HttpResponseRedirect
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import Comment, User, Listing, Bid, Watchlist


class CreateForm(forms.Form):
    title = CharField(max_length=64)
    description = CharField(widget=Textarea)
    start = IntegerField(min_value=0)
    thumbnail = CharField(max_length=256, required=False)
    category = ChoiceField(choices=Listing.CATEGORIES, required=False)


class BidForm(forms.Form):
    bid = IntegerField()


class CommentForm(forms.Form):
    comment = CharField(widget=Textarea)


def get_top_bidder(listing):
    return Bid.objects.filter(listing=listing).order_by("-price").first().owner


def get_top_bid(listing):
    return Bid.objects.filter(listing=listing).aggregate(Max("price"))["price__max"]


def redirect_to_listing(id):
    return HttpResponseRedirect(reverse("listings", args=[id]))


def index(request):
    dict_categ = dict(Listing.CATEGORIES)
    return render(request, "auctions/index.html", {
        "listings": [{"price": get_top_bid(listing), "listing": listing, "category": dict_categ[listing.category]} for listing in Listing.objects.filter(closed=False)],
        "categories": dict(Listing.CATEGORIES)
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            listing = Listing(
                owner=request.user, name=form.cleaned_data["title"], thumbnail=form.cleaned_data["thumbnail"], description=form.cleaned_data["description"], category=form.cleaned_data["category"])
            listing.save()
            startbid = Bid(
                listing=listing, price=form.cleaned_data["start"], owner=request.user)
            startbid.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            raise SuspiciousOperation()

    else:
        return render(request, 'auctions/create.html', {
            "form": CreateForm()
        })


def listings(request, id):
    listing = get_object_or_404(Listing, pk=id)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "price": get_top_bid(listing),
        "form": BidForm(),
        "winning": get_top_bidder(listing),
        "comments": Comment.objects.filter(listing=listing)
    })


@login_required
def toggle(request, id):
    try:
        Watchlist.objects.get(
            listing=get_object_or_404(Listing, pk=id), owner=request.user).delete()
    except ObjectDoesNotExist:
        Watchlist(listing=get_object_or_404(
            Listing, pk=id), owner=request.user).save()
    return redirect_to_listing(id)


@login_required
def bid(request, id):
    form = BidForm(request.POST)
    listing = get_object_or_404(
        Listing, pk=id)
    if form.is_valid() and form.cleaned_data["bid"] > get_top_bid(listing) and not listing.closed:
        Bid(price=form.cleaned_data["bid"],
            listing=listing, owner=request.user).save()

        return redirect_to_listing(id)
    else:
        raise SuspiciousOperation()


@login_required
def close(request, id):
    listing = get_object_or_404(Listing, pk=id)
    listing.closed = True
    listing.save()
    return redirect_to_listing(id)


@login_required
def comment(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        Comment(listing=get_object_or_404(Listing, pk=id),
                owner=request.user, text=form.cleaned_data["comment"]).save()
        return redirect_to_listing(id)
    else:
        return SuspiciousOperation()


@login_required
def watchlist(request):
    dict_categ = dict(Listing.CATEGORIES)
    return render(request, "auctions/watchlist.html", {
        "listings": [{"price": get_top_bid(listing), "listing": listing, "category": dict_categ[listing.category]} for listing in Listing.objects.filter(watchlist__owner=request.user)],
        "categories": dict(Listing.CATEGORIES)
    })


def categories(request):
    return render(request, 'auctions/categories.html', {
        "categories": Listing.CATEGORIES
    })


def category(request, category):
    dict_categ = dict(Listing.CATEGORIES)
    return render(request, "auctions/category.html", {
        "listings": [{"price": get_top_bid(listing), "listing": listing, "category": dict_categ[listing.category]} for listing in Listing.objects.filter(category=category, closed=False)],
        "category": dict_categ[category]
    })
