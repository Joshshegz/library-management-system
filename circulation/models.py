from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import BookCopy


def default_loan_days():
    return getattr(settings, "LIBRARY_LOAN_DAYS", 14)


class Loan(models.Model):
    borrower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="loans",
    )
    book_copy = models.ForeignKey(
        BookCopy,
        on_delete=models.PROTECT,
        related_name="loans",
    )
    borrowed_at = models.DateTimeField(default=timezone.now)
    due_at = models.DateTimeField()
    returned_at = models.DateTimeField(null=True, blank=True)
    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="loans_issued",
    )

    class Meta:
        ordering = ["-borrowed_at"]

    def __str__(self):
        return f"{self.borrower.matric_no} — {self.book_copy.copy_code}"

    def save(self, *args, **kwargs):
        if self.due_at is None:
            base = self.borrowed_at or timezone.now()
            self.due_at = base + timedelta(days=default_loan_days())
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.returned_at is None

    @property
    def is_overdue(self):
        return self.is_active and timezone.now() > self.due_at

    @property
    def book(self):
        return self.book_copy.book
