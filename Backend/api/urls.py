from django.urls import path
from rest_framework import routers
from .views import BookViewSet, AutherViewSet, PublisherViewSet, GenreViewSet, CustomUserViewSet, BorrowedBookViewSet, BookReviewViewSet, NotificationViewSet, FeedbackViewSet, WishlistViewSet


router = routers.DefaultRouter()    # automatic URL routing for viewsets

router.register(r'books', BookViewSet)
router.register(r'authors', AutherViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'borrowed-books', BorrowedBookViewSet)
router.register(r'book-reviews', BookReviewViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'wishlists', WishlistViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = router.urls