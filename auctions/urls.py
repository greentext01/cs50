from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:id>", views.listings, name="listings"),
    path("toggle-watchlist/<int:id>", views.toggle, name="toggle-watchlist"),
    path("close/<int:id>", views.close, name="close"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("categories/", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("comment/<int:id>", views.comment, name="comment")
]
