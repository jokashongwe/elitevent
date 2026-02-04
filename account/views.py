from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import RegisterForm, LoginForm

# Vue d'Inscription
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # On connecte l'utilisateur directement après l'inscription
            login(request, user)
            return redirect('dashboard_home')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

# Vue de Connexion personnalisée pour utiliser notre LoginForm
class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'