from django.contrib import admin
from .models import Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification, Feedback
# Register your models here.

for model in [Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification, Feedback]:
    admin.site.register(model)