from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookCopyForm, BookForm
from .models import Book, BookCopy


def librarian_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if not request.user.is_librarian:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapper


@login_required
def book_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()

    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(isbn__icontains=query)
            | Q(category__icontains=query)
        )
    if category:
        books = books.filter(category__iexact=category)

    categories = (
        Book.objects.exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    return render(
        request,
        "catalog/book_list.html",
        {
            "books": books,
            "query": query,
            "category": category,
            "categories": categories,
            "nav_active": "catalogue",
            "search_query": query,
        },
    )


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    copy_form = None
    if request.user.is_librarian:
        copy_form = BookCopyForm()

    if request.method == "POST" and request.user.is_librarian:
        copy_form = BookCopyForm(request.POST)
        if copy_form.is_valid():
            copy = copy_form.save(commit=False)
            copy.book = book
            copy.save()
            messages.success(request, f"Copy {copy.copy_code} added.")
            return redirect("catalog:book_detail", pk=book.pk)

    return render(
        request,
        "catalog/book_detail.html",
        {
            "book": book,
            "copy_form": copy_form,
            "nav_active": "catalogue",
            "search_query": request.GET.get("q", "").strip(),
        },
    )


@login_required
@librarian_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f"“{book.title}” added to catalogue.")
            return redirect("catalog:book_detail", pk=book.pk)
    else:
        form = BookForm()

    return render(
        request,
        "catalog/book_form.html",
        {
            "form": form,
            "title": "Add book",
            "nav_active": "catalogue",
            "search_query": request.GET.get("q", "").strip(),
        },
    )


@login_required
@librarian_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect("catalog:book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)

    return render(
        request,
        "catalog/book_form.html",
        {
            "form": form,
            "title": "Edit book",
            "book": book,
            "nav_active": "catalogue",
            "search_query": request.GET.get("q", "").strip(),
        },
    )


@login_required
@librarian_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        title = book.title
        book.delete()
        messages.success(request, f"“{title}” removed from catalogue.")
        return redirect("catalog:book_list")
    return render(
        request,
        "catalog/book_confirm_delete.html",
        {
            "book": book,
            "nav_active": "catalogue",
            "search_query": request.GET.get("q", "").strip(),
        },
    )
