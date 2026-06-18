from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from catalog.models import BookCopy

from .models import Loan


class LoanError(ValidationError):
    pass


def user_active_loan_count(user):
    return Loan.objects.filter(borrower=user, returned_at__isnull=True).count()


@transaction.atomic
def borrow_copy(*, borrower, book_copy, issued_by=None, max_loans=5):
    copy = BookCopy.objects.select_for_update().get(pk=book_copy.pk)

    if copy.status != BookCopy.Status.AVAILABLE:
        raise LoanError("This copy is not available to borrow.")

    if user_active_loan_count(borrower) >= max_loans:
        raise LoanError(f"You may borrow at most {max_loans} books at a time.")

    if Loan.objects.filter(
        borrower=borrower, book_copy=copy, returned_at__isnull=True
    ).exists():
        raise LoanError("You already have an active loan for this copy.")

    now = timezone.now()
    loan = Loan.objects.create(
        borrower=borrower,
        book_copy=copy,
        borrowed_at=now,
        issued_by=issued_by,
    )

    copy.status = BookCopy.Status.ON_LOAN
    copy.save(update_fields=["status"])

    return loan


@transaction.atomic
def return_loan(*, loan):
    loan = Loan.objects.select_for_update().select_related("book_copy").get(pk=loan.pk)

    if not loan.is_active:
        raise LoanError("This loan has already been returned.")

    now = timezone.now()
    loan.returned_at = now
    loan.save(update_fields=["returned_at"])

    copy = loan.book_copy
    copy.status = BookCopy.Status.AVAILABLE
    copy.save(update_fields=["status"])

    return loan
