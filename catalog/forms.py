from django import forms

from .models import Book, BookCopy


class BookForm(forms.ModelForm):
    def clean_isbn(self):
        value = (self.cleaned_data.get("isbn") or "").strip()
        return value or None

    class Meta:
        model = Book
        fields = (
            "title",
            "author",
            "isbn",
            "category",
            "publisher",
            "publication_year",
            "description",
        )
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "isbn": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.TextInput(attrs={"class": "form-control"}),
            "publisher": forms.TextInput(attrs={"class": "form-control"}),
            "publication_year": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class BookCopyForm(forms.ModelForm):
    class Meta:
        model = BookCopy
        fields = ("copy_code", "shelf_location", "status")
        widgets = {
            "copy_code": forms.TextInput(attrs={"class": "form-control"}),
            "shelf_location": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }
