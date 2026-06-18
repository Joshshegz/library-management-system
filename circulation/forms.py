from django import forms

from catalog.models import BookCopy


class BorrowCopyForm(forms.Form):
    copy = forms.ModelChoiceField(
        queryset=BookCopy.objects.none(),
        label="Select copy",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, book, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["copy"].queryset = book.copies.filter(
            status=BookCopy.Status.AVAILABLE
        )
