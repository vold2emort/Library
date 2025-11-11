from rest_framework import serializers

from Books.models import Book, User


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'genres',]


class UserSerializer(serializers.ModelSerializer):
    borrowed_books = BookSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'borrowed_books']