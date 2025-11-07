from django.urls import path

from .views import BookApiView, BookApiDetail

urlpatterns = [
    path('', BookApiView.as_view()),
    path('<int:pk>', BookApiDetail.as_view()),
]