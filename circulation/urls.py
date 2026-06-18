from django.urls import path

from . import views

app_name = "circulation"

urlpatterns = [
    path("my-loans/", views.my_loans, name="my_loans"),
    path("borrow/<int:book_pk>/", views.borrow_book, name="borrow_book"),
    path("return/<int:loan_pk>/", views.return_book, name="return_book"),
    path("manage/", views.manage_loans, name="manage_loans"),
]
