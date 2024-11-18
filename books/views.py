from django.db.models import Count, Q, Subquery, OuterRef
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.models import CustomUser
from .models import Book, Author, Genre, BookCheckout
from books.permissions import IsStaffUser, IsAuthorOrStaff
from .serializers import (BookSerializer, AuthorSerializer, GenreSerializer, BookCheckoutSerializer,
                          BookCheckoutCreateSerializer, BookCheckoutUpdateSerializer)
from .filters import BookFilter

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [IsStaffUser]
        return [permission() for permission in permission_classes]


class BookCheckoutViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    queryset = BookCheckout.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookCheckoutSerializer
        elif self.action == 'create':
            return BookCheckoutCreateSerializer
        elif self.action == 'update':
            return BookCheckoutUpdateSerializer
        return super().get_serializer_class()


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    permission_classes = [IsAuthorOrStaff]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class BookStatsView(APIView):
    def get(self, request):
        stats = {
            'most_popular_books': self.get_most_popular_books(),
            'book_checkouts_last_year': self.get_book_checkouts_last_year(),
            'late_books': self.get_late_books(),
            'late_users': self.get_late_users(),
        }
        return Response(stats)

    @staticmethod
    def get_book_checkouts_last_year():
        one_year_ago = timezone.now() - timezone.timedelta(days=365)
        book_checkouts_last_year = BookCheckout.objects.filter(
            checkout_date__gte=one_year_ago
        ).values('book').annotate(
            total_checkouts=Count('id')
        ).order_by('book')
        return list(book_checkouts_last_year)

    @staticmethod
    def get_late_books():
        late_book_checkouts = Book.objects.annotate(
            late_count=Count(
                'checkouts',
                filter=Q(checkouts__is_late=True)
            )
        ).order_by('-late_count')[:100]
        return BookSerializer(late_book_checkouts, many=True).data

    @staticmethod
    def get_late_users():
        late_user_checkouts = CustomUser.objects.annotate(
            late_count=Count(
                'book_checkouts',
                filter=Q(
                    book_checkouts__is_returned=True,
                    book_checkouts__return_date__gt=Subquery(
                        BookCheckout.objects.filter(
                            user=OuterRef('pk'),
                            is_returned=True,
                        ).values('checkout_date')[:1]
                    )
                )
            )
        ).order_by('-late_count')[:100]
        return [
            {
                'id': user.id,
                'username': user.username,
                'late_count': user.late_count
            }
            for user in late_user_checkouts
        ]

    @staticmethod
    def get_most_popular_books():
        most_popular_books = Book.objects.annotate(
            total_checkouts=Count('checkouts')
        ).order_by('-total_checkouts')[:10]
        return BookSerializer(most_popular_books, many=True).data
