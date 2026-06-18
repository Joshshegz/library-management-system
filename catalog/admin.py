from django.contrib import admin

from .models import Book, BookCopy


class BookCopyInline(admin.TabularInline):
    model = BookCopy
    extra = 1


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "category", "copy_count")
    list_filter = ("category",)
    search_fields = ("title", "author", "isbn")
    inlines = [BookCopyInline]

    @admin.display(description="Copies")
    def copy_count(self, obj):
        return obj.total_copies


@admin.register(BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ("copy_code", "book", "shelf_location", "status")
    list_filter = ("status",)
    search_fields = ("copy_code", "book__title", "book__author")
