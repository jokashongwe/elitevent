from django import forms
from .models import Event, Guest, DrinkOption
from django.forms import inlineformset_factory

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'event_type', 'date', 'location','cover_image', 'theme_template']
        
        # C'est ici que la magie Tailwind opère
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Ex: Mariage de Sophie & Thomas'
            }),
            'event_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white'
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'type': 'datetime-local'  # Active le sélecteur de date natif du navigateur
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Ex: Château de la Loire ou Zoom'
            }),
            'theme_template': forms.Select(attrs={ # Si c'est un choix
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 bg-white'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer'
            }),
        }
        labels = {
            'title': 'Titre de l\'événement',
            'event_type': 'Type d\'événement',
            'date': 'Date et Heure',
            'location': 'Lieu',
            'theme_template': 'Modèle d\'invitation'
        }

class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['full_name', 'email', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500',
                'placeholder': 'Jean Dupont'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500',
                'placeholder': 'jean@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500',
                'placeholder': '+243....'
            }),
        }

class GuestImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Fichier CSV (Nom, Email)",
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
        })
    )

class DrinkOptionForm(forms.ModelForm):
    class Meta:
        model = DrinkOption
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Ex: Champagne'
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500',
                'placeholder': 'Cuvée spéciale 2018 (Optionnel)'
            }),
        }

# La "Factory" qui lie l'Event aux DrinkOptions
DrinkOptionFormSet = inlineformset_factory(
    Event, 
    DrinkOption, 
    form=DrinkOptionForm,
    fields=['name', 'description'],
    extra=1,          # Affiche toujours 1 ligne vide pour ajouter une nouvelle boisson
    can_delete=True   # Permet de cocher une case pour supprimer
)