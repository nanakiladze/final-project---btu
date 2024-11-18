from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import CustomUser
from books.models import Book


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=255, required=True)
    surname = forms.CharField(max_length=255, required=True)
    birth_date = forms.DateField(required=True)
    personal_number = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'name', 'surname', 'birth_date', 'personal_number']

    def save(self, commit=True):
        user = super().save()
        print(user)
        user.first_name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['surname']
        user.save(update_fields=['first_name', 'last_name'])

        return user


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
