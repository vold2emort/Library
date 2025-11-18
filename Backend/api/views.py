from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions

from Books.models import Book, Author, Publisher, Genre, CustomUser, BorrowedBook, BookReview, Notification, Feedback, Wishlist
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer, GenreSerializer, CustomUserSerializer, BorrowedBookSerializer, BookReviewSerializer, NotificationSerializer, FeedbackSerializer, WishlistSerializer


# Create your views here.

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    http_method_names = ['get']  # only allow GET requests, HEAD, OPTIONS are allowed by default

    # DRF filters (complex filtering than custom ones) - less code, more functionality
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Fields to filter by query params
    filterset_fields = ['author__name', 'genre__name', 'publisher__name', 'published_date'] # /?author__name=AuthorName&genre__name=GenreName
    # Ordering fields
    ordering_fields = ['published_date', 'title']   # /?ordering=-published_date 
    # Search fields
    search_fields = ['title', 'author__name', 'genre__name', 'publisher__name']     # /?search=keyword


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
    http_method_names = ['get', 'post', 'delete', 'patch']

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
    http_method_names = ['get', 'post', 'delete']

    queryset = Notification.objects.none()  # to avoid DRF router basename warning
    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, *args, **kwargs):
        notification_obj = self.get_object()
        notification_obj.is_read = True
        notification_obj.save()
        return Response({'message': 'Notification marked as read.'}, status=200)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request, *args, **kargs):
        user_unread_notifications = Notification.objects.filter(receiver=request.user, is_read=False)
        for notification_obj in user_unread_notifications:
            notification_obj.is_read = True
            notification_obj.save()
        return Response({'message': f'All ({len(user_unread_notifications)}) Unread Notifications marked as read.'}, status=200)
    
    @action(detail=False, methods=['delete'])
    def delete_all(self, request, *args, **kargs):
        user_notifications = Notification.objects.filter(receiver=request.user)
        deleted_count, _ = user_notifications.delete()
        return Response({'message': f'All ({deleted_count}) notifications deleted.'}, status=200)
    
    # prevent single notification deletion
    def destroy(self, request, *args, **kwargs):
        raise NotImplementedError("Single notification deletion is not allowed. Use delete_all action to delete all notifications.")
    # prevent creation of notifications via API
    def create(self, request, *args, **kwargs):
        raise NotImplementedError("Creating notifications via API is not allowed.")
    

    ''' Future Update: Only allow librarian/admin to create notifications for users
    def create(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'error': 'Only librarians/admins can create notifications.'}, status=403)
        return super().create(request, *args, **kwargs)
    '''


class FeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = FeedbackSerializer
    http_method_names = ['post']

    queryset = Feedback.objects.none()  # no get requests allowed so empty queryset

class WishlistViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WishlistSerializer
    http_method_names = ['get', 'post', 'delete']    # (block wishlist deletion)

    queryset = Wishlist.objects.none()
    def get_queryset(self): # only show wishlist of logged in user
        return Wishlist.objects.filter(user=self.request.user)
    
    # prevent deletion of wishlist, only clear items
    def destroy(self, request, *args, **kwargs):
        return Response({'error': 'Wishlist deletion is not allowed. You can clear items using PATCH.'}, status=403)


    @action(detail=True, methods=['post', 'delete'], url_path='books/(?P<book_id>[0-9]+)')  # /api/v1/wishlists/{pk}/books/{book_id}/
    def add_remove_book(self, request, pk=None , book_id=None):
        wishlist_obj = self.get_object()
        if not book_id:
            return Response({'error': 'book_id is required.'}, status=400)

        book_id = int(book_id)        
        current_books = wishlist_obj.books.values_list('id', flat=True)        
        if request.method.lower() == 'post':
            if book_id in current_books:
                return Response({'message': 'Book already in wishlist.'}, status=200)
            wishlist_obj.books.add(book_id)     # add book to wishlist (filter duplicates automatically behaves as set)
            # wishlist_obj.save()   # unnecessary for M2M relations
            return Response({'message': 'Book added to wishlist.'}, status=200)
        
        if request.method.lower() == 'delete':
            if book_id not in current_books:
                return Response({'message': 'Book not found in wishlist.'}, status=404)
            wishlist_obj.books.remove(book_id)  # remove book from wishlist
            return Response({'message': 'Book removed from wishlist.'}, status=200)
        