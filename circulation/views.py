from django.contrib import messages
from django.contrib.auth.decorators import login_required

from biometrics.decorators import biometric_enrolled_required
from biometrics.verification import NoseVerificationError, verify_user_nose
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Book

from .forms import BorrowCopyForm
from .models import Loan
from .services import LoanError, borrow_copy, return_loan


def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_librarian:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def my_loans(request):
    active = (
        Loan.objects.filter(borrower=request.user, returned_at__isnull=True)
        .select_related("book_copy__book")
        .order_by("due_at")
    )
    history = (
        Loan.objects.filter(borrower=request.user, returned_at__isnull=False)
        .select_related("book_copy__book")[:8]
    )
    now = timezone.now()
    overdue_count = sum(1 for loan in active if loan.is_overdue)
    next_due = active.first()
    return render(
        request,
        "circulation/my_loans.html",
        {
            "nav_active": "loans",
            "active_loans": active,
            "history_loans": history,
            "overdue_count": overdue_count,
            "next_due": next_due,
            "search_query": request.GET.get("q", "").strip(),
        },
    )


@login_required
@biometric_enrolled_required
def borrow_book(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    available = book.copies.filter(status="available")

    if not available.exists():
        messages.error(request, "No copies are available for this book.")
        return redirect("catalog:book_detail", pk=book.pk)
        
    if request.user.is_librarian:
        messages.error(request, "Librarians are not allowed to borrow books.")
        return redirect("catalog:book_detail", pk=book.pk)

    if request.method == "POST":
        try:
            verify_user_nose(request.user, request)
        except NoseVerificationError as exc:
            messages.error(request, str(exc))
            form = BorrowCopyForm(book, request.POST)
            return render(
                request,
                "circulation/borrow.html",
                {"book": book, "form": form, "nav_active": "catalogue"},
            )

        form = BorrowCopyForm(book, request.POST)
        if form.is_valid():
            try:
                loan = borrow_copy(
                    borrower=request.user,
                    book_copy=form.cleaned_data["copy"],
                    issued_by=request.user if request.user.is_librarian else None,
                )
                messages.success(
                    request,
                    f"Borrowed “{book.title}” ({loan.book_copy.copy_code}). "
                    f"Due {loan.due_at.strftime('%d %b %Y')}.",
                )
                return redirect("circulation:my_loans")
            except (LoanError, ValidationError) as exc:
                messages.error(request, str(exc))
    else:
        form = BorrowCopyForm(book)

    return render(
        request,
        "circulation/borrow.html",
        {"book": book, "form": form, "nav_active": "catalogue"},
    )


@login_required
@biometric_enrolled_required
def return_book(request, loan_pk):
    loan = get_object_or_404(Loan, pk=loan_pk)

    if loan.borrower != request.user and not request.user.is_librarian:
        raise PermissionDenied

    if request.method == "POST":
        try:
            verify_user_nose(request.user, request)
        except NoseVerificationError as exc:
            messages.error(request, str(exc))
            return render(
                request,
                "circulation/return_confirm.html",
                {
                    "loan": loan,
                    "nav_active": "loans",
                    "today": timezone.localdate(),
                },
            )

        try:
            return_loan(loan=loan)
            messages.success(
                request,
                f"Returned “{loan.book.title}” ({loan.book_copy.copy_code}).",
            )
            if request.user.is_librarian and request.POST.get("next") == "manage":
                return redirect("circulation:manage_loans")
            return redirect("circulation:my_loans")
        except (LoanError, ValidationError) as exc:
            messages.error(request, str(exc))

    return render(
        request,
        "circulation/return_confirm.html",
        {
            "loan": loan,
            "nav_active": "loans",
            "today": timezone.localdate(),
        },
    )


@login_required
@librarian_required
def manage_loans(request):
    show = request.GET.get("show", "active")
    loans = Loan.objects.select_related(
        "borrower", "book_copy", "book_copy__book"
    )

    if show == "overdue":
        loans = loans.filter(returned_at__isnull=True, due_at__lt=timezone.now())
        title = "Overdue loans"
    elif show == "all":
        loans = loans.all()[:100]
        title = "All loans (recent)"
    else:
        loans = loans.filter(returned_at__isnull=True)
        title = "Active loans"

    return render(
        request,
        "circulation/manage_loans.html",
        {"loans": loans, "title": title, "show": show},
    )
