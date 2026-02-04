from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Mixin pour éviter de répéter le style sur chaque champ
class TailwindStyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm'

class LoginForm(TailwindStyleMixin, AuthenticationForm):
    """Formulaire de connexion stylisé"""
    pass

class RegisterForm(TailwindStyleMixin, UserCreationForm):
    """Formulaire d'inscription stylisé"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')