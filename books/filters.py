from django_filters import rest_framework as filters
from .models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author = filters.CharFilter(field_name='author__last_name', lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genre__name', lookup_expr='icontains')
    publication_date = filters.DateFromToRangeFilter()
    stock_quantity = filters.RangeFilter()

    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'publication_date', 'stock_quantity')
