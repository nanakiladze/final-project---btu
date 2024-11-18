from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, AuthorViewSet, GenreViewSet, BookCheckoutViewSet, BookStatsView

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'checkout', BookCheckoutViewSet, basename='checkout')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/stats/', BookStatsView.as_view(), name='book-stats'),
]