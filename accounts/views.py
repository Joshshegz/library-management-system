from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from datetime import timedelta

from django.utils import timezone

from biometrics.enrollment import has_nose_template, has_windows_hello, is_fully_enrolled
from catalog.models import Book, BookCopy
from circulation.models import Loan

from .forms import MatricAuthenticationForm, UserProfileForm, UserRegistrationForm
from .models import User


def home(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    today = timezone.localdate()
    return render(
        request,
        "accounts/home.html",
        {
            "books_available": BookCopy.objects.filter(
                status=BookCopy.Status.AVAILABLE
            ).count(),
            "active_members": User.objects.filter(is_active=True).count(),
            "loans_today": Loan.objects.filter(borrowed_at__date=today).count(),
            "title_count": Book.objects.count(),
        },
    )


class MatricLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = MatricAuthenticationForm
    redirect_authenticated_user = True


class MatricLogoutView(LogoutView):
    next_page = reverse_lazy("home")


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Account created. Complete biometric enrollment next.",
            )
            return redirect("biometrics:enroll")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    now = timezone.now()
    soon = now + timedelta(days=3)
    active_loans = (
        Loan.objects.filter(borrower=request.user, returned_at__isnull=True)
        .select_related("book_copy__book")
        .order_by("due_at")
    )
    due_soon_count = active_loans.filter(due_at__lte=soon).count()
    recent_loans = active_loans[:3]

    hello_done = has_windows_hello(request.user)
    nose_done = has_nose_template(request.user)
    if hello_done and nose_done:
        enrol_pct = 100
    elif hello_done:
        enrol_pct = 50
    else:
        enrol_pct = 0

    hour = timezone.localtime(now).hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 17:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    return render(
        request,
        "accounts/dashboard.html",
        {
            "nav_active": "dashboard",
            "greeting": greeting,
            "active_loan_count": active_loans.count(),
            "due_soon_count": due_soon_count,
            "recent_loans": recent_loans,
            "fully_enrolled": is_fully_enrolled(request.user),
            "hello_done": hello_done,
            "nose_done": nose_done,
            "enrol_pct": enrol_pct,
            "title_count": Book.objects.count(),
        },
    )


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(
        request,
        "accounts/profile.html",
        {"form": form, "nav_active": "profile"},
    )
