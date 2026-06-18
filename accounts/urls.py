from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.MatricLoginView.as_view(), name="login"),
    path("logout/", views.MatricLogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
]
