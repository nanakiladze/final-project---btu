from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from accounts.models import CustomUser


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    stock_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    @property
    def all_times_checked_out(self):
        return self.checkouts.count()

    @property
    def available_copies(self):
        # stock quantity - number of copies that are currently checked out
        return self.stock_quantity - self.checkouts.filter(is_returned=False).count()

    @property
    def recently_checked_out_copies(self):
        return self.checkouts.filter(is_returned=False).count()


class BookCheckout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='checkouts')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='book_checkouts')
    checkout_date = models.DateTimeField(auto_now_add=True)
    is_taken = models.BooleanField(default=False)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
