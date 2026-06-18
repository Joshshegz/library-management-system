from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("add/", views.book_create, name="book_create"),
    path("<int:pk>/", views.book_detail, name="book_detail"),
    path("<int:pk>/edit/", views.book_edit, name="book_edit"),
    path("<int:pk>/delete/", views.book_delete, name="book_delete"),
]
