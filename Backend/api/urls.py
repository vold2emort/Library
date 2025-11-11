from django.urls import path

from .views import BookApiView, BookApiDetail, UserBookView

urlpatterns = [
    path('', BookApiView.as_view()),
    path('<int:pk>', BookApiDetail.as_view()),
    path('books/', UserBookView.as_view()), 
]