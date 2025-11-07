from rest_framework import generics

from Books.models import Book
from .serializers import BookSerializer
# Create your views here.


class BookApiView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookApiDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer