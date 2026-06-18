from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class MatricAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Matric Number",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. 2021000382",
                "autocomplete": "username",
                "class": "form-control login-field",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
                "class": "form-control login-field",
                "id": "id_password",
            }
        ),
    )

    def clean_username(self):
        return self.cleaned_data["username"].strip().upper()


DEPARTMENT_CHOICES = [
    ("", "Select department"),
    ("Computer Science", "Computer Science"),
    ("Information Science", "Information Science"),
    ("Mathematics", "Mathematics"),
    ("Statistics", "Statistics"),
    ("Other", "Other"),
]


class UserRegistrationForm(UserCreationForm):
    matric_no = forms.CharField(
        label="Matric Number",
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. 2021000382",
                "class": "form-control reg-field",
            }
        ),
    )
    first_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "As written on student ID",
                "class": "form-control reg-field",
            }
        ),
    )
    last_name = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "student@lautech.edu.ng",
                "class": "form-control reg-field",
            }
        ),
    )
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control reg-field reg-select"}),
    )
    phone = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control reg-field", "placeholder": "••••••••"}
        ),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control reg-field", "placeholder": "••••••••"}
        ),
    )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("first_name") and not cleaned.get("last_name"):
            cleaned["last_name"] = cleaned["first_name"].split()[-1][:50]
        return cleaned

    class Meta:
        model = User
        fields = (
            "matric_no",
            "first_name",
            "last_name",
            "email",
            "department",
            "phone",
            "password1",
            "password2",
        )

    def clean_matric_no(self):
        return self.cleaned_data["matric_no"].strip().upper()


class UserProfileForm(forms.ModelForm):
    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control profile-field"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "department", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control profile-field"}),
            "last_name": forms.HiddenInput(),
            "email": forms.EmailInput(attrs={"class": "form-control profile-field"}),
            "phone": forms.HiddenInput(),
        }
