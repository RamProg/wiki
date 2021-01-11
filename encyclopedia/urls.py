from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/search/results.html", views.search, name="search"),
    path("new", views.new, name="new"),
    path("create", views.create, name="create"),
    path("wiki/editor/<str:title>", views.editor, name="editor"),
    path("random", views.random, name="random")
]
