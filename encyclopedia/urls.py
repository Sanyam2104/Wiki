from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>/", views.titleSearch, name="titleSearch"),
    path("new_entry", views.new_entry, name="new_entry"),
    path("random", views.random_page, name="random"),
    path("search", views.search_bar, name="search"),
    path("edit/<str:title>", views.edit_entry, name="edit_entry")
]
