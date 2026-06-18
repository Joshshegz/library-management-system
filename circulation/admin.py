from django.contrib import admin

from .models import Loan


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = (
        "book_copy",
        "borrower",
        "borrowed_at",
        "due_at",
        "returned_at",
        "is_overdue_display",
    )
    list_filter = ("returned_at", "borrowed_at")
    search_fields = (
        "borrower__matric_no",
        "borrower__first_name",
        "borrower__last_name",
        "book_copy__copy_code",
        "book_copy__book__title",
    )
    raw_id_fields = ("borrower", "book_copy", "issued_by")
    date_hierarchy = "borrowed_at"

    @admin.display(boolean=True, description="Overdue")
    def is_overdue_display(self, obj):
        return obj.is_overdue
