from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Votre Nom", max_length=100, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:bg-white focus:ring-0'}))
    email = forms.EmailField(label="Votre Email", widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:bg-white focus:ring-0'}))
    message = forms.CharField(label="Parlez-nous de votre projet", widget=forms.Textarea(attrs={'class': 'w-full px-4 py-3 rounded-lg bg-gray-50 border border-gray-200 focus:border-indigo-500 focus:bg-white focus:ring-0', 'rows': 4}))