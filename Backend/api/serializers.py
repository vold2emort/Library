from rest_framework import serializers

from Books.models import Book


class BookSerializer(serializers.ModelSerializer):
    authors = serializers.StringRelatedField(many=True)
    genres = serializers.StringRelatedField(many=True)
    class Meta:
        model = Book
        fields = ('id', 'title', 'authors', 'genres',)