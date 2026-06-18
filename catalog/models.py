from django.db import models
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField("ISBN", max_length=20, blank=True, unique=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    publisher = models.CharField(max_length=150, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"

    def get_absolute_url(self):
        return reverse("catalog:book_detail", kwargs={"pk": self.pk})

    @property
    def total_copies(self):
        return self.copies.count()

    @property
    def available_copies(self):
        return self.copies.filter(status=BookCopy.Status.AVAILABLE).count()


class BookCopy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        ON_LOAN = "on_loan", "On loan"
        LOST = "lost", "Lost"
        MAINTENANCE = "maintenance", "Under maintenance"

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="copies")
    copy_code = models.CharField(
        max_length=30,
        unique=True,
        help_text="Unique shelf/barcode ID for this copy.",
    )
    shelf_location = models.CharField(max_length=50, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["copy_code"]
        verbose_name_plural = "book copies"

    def __str__(self):
        return f"{self.copy_code} ({self.book.title})"
