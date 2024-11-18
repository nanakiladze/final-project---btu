from typing import List, Dict

from django.contrib.auth import login, logout
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from rest_framework import status

from accounts.forms import UserRegistrationForm, UserLoginForm


import requests
from books.models import Book, BookCheckout


class BookService:
    API_URL = 'http://127.0.0.1:8000/books/api/books/'
    ERROR_CODES = {status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND, status.HTTP_500_INTERNAL_SERVER_ERROR}

    @classmethod
    def fetch_books(cls) -> tuple[List, str]:
        try:
            response = requests.get(cls.API_URL)
            if response.status_code in cls.ERROR_CODES:
                return [], response.json().get('detail', 'Unknown error')
            return response.json(), ''
        except requests.RequestException as e:
            return [], str(e)

    @staticmethod
    def get_book_statuses(books: List) -> Dict:
        book_statuses = {}
        for book in books:
            book_id = book['id']
            is_reserved = BookCheckout.objects.filter(
                book_id=book_id,
                return_date__isnull=True
            ).exists()
            book_statuses[book_id] = 'reserved' if is_reserved else 'available'
        return book_statuses


class HomeView(View):
    template_name = 'home.html'
    items_per_page = 10

    def get(self, request):
        books, error = BookService.fetch_books()

        if error:
            messages.error(request, error)
            return redirect('login')

        book_statuses = BookService.get_book_statuses(books)
        paginator = Paginator(books, self.items_per_page)
        page_obj = paginator.get_page(request.GET.get('page'))

        context = {
            'page_obj': page_obj,
            'book_statuses': book_statuses,
        }
        return render(request, self.template_name, context)


class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = 'login'

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class()
        })

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': self.form_class()
        })

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('admin:index' if user.is_staff else 'home')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, 'You have been logged out.')
        return redirect('login')
