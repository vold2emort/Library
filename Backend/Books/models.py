from django.db import models

from django.contrib.auth.models import AbstractUser
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=250)
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')

    def __str__(self):
        return self.title


class User(AbstractUser):
    borrowed_books = models.OneToOneField(
        Book,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="borrower"
    )

    def __str__(self):
        return self.username