from django.utils import timezone
from rest_framework import serializers
from .models import Book, Author, Genre, BookCheckout


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'publication_date', 'stock_quantity']


class BookCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCheckout
        fields = ['id', 'book', 'user', 'checkout_date', 'is_returned']


class BookCheckoutCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCheckout
        fields = ['book', 'user']


class BookCheckoutUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCheckout
        fields = ['is_taken', 'is_returned']

    def update(self, instance, validated_data):
        is_returned = validated_data.get('is_returned')
        if is_returned:
            instance.return_date = timezone.now()
        return super().update(instance, validated_data)
