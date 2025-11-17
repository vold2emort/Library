from django.contrib import admin
from .models import Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification
# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(CustomUser)
admin.site.register(BorrowedBook)
admin.site.register(BookReview)
admin.site.register(Notification)