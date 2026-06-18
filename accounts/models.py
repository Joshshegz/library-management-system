from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, matric_no, password=None, **extra_fields):
        if not matric_no:
            raise ValueError("Matric number is required.")
        matric_no = matric_no.strip().upper()
        user = self.model(matric_no=matric_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_no, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", User.Role.LIBRARIAN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(matric_no, password, **extra_fields)


class User(AbstractUser):
    """LAUTECH library user — login with matric number (Staff/Student ID)."""

    class Role(models.TextChoices):
        MEMBER = "member", "Student / Member"
        LIBRARIAN = "librarian", "Librarian"

    username = None

    matric_no = models.CharField(
        "Staff/Student ID",
        max_length=20,
        unique=True,
        help_text="e.g. 2021000382",
    )
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    department = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    biometric_enrolled = models.BooleanField(
        default=False,
        help_text="True after nose + thumb templates are saved.",
    )

    USERNAME_FIELD = "matric_no"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()

    class Meta:
        ordering = ["matric_no"]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return f"{self.matric_no} — {self.get_full_name()}"

    @property
    def is_librarian(self):
        return self.role == self.Role.LIBRARIAN or self.is_superuser

    @property
    def is_member(self):
        return self.role == self.Role.MEMBER
