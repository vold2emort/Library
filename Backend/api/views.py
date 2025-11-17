from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions

from Books.models import Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer, GenreSerializer, CustomUserSerializer, BorrowedBookSerializer, BookReviewSerializer, NotificationSerializer


# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get']  # only allow GET requests, HEAD, OPTIONS are allowed by default

    # DRF filters (complex filtering than custom ones) - less code, more functionality
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Fields to filter by
    filterset_fields = ['author__name', 'genre__name', 'publisher__name', 'published_date']
    # Ordering fields
    ordering_fields = ['published_date', 'title']
    # Search fields
    search_fields = ['title', 'author__name', 'genre__name', 'publisher__name']


class AutherViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    http_method_names = ['get']

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    http_method_names = ['get']

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get']

class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get']

from rest_framework.decorators import action
from rest_framework.response import Response

class BorrowedBookViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    http_method_names = ['get', 'post', 'delete']

    queryset = BorrowedBook.objects.none()  # to avoid basename warning in router else have to set basename in router

    # only show borrowed books of logged in user
    def get_queryset(self):
        return BorrowedBook.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])   # custom action at /api/v1/borrowed-books/info/    
    def info(self, request):
        return Response({"message": "Hello, this is your borrowed books info!"})


class BookReviewViewSet(viewsets.ModelViewSet):
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    http_method_names = ['get', 'post']


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    http_method_names = ['get', 'delete']

    queryset = Notification.objects.none()  # to avoid DRF router basename warning
    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)