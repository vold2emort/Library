from rest_framework import serializers
from Books.models import Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification, Feedback, Wishlist


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']  # Exclude password from being exposed

class BorrowedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBook
        fields = '__all__'


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
    
class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'