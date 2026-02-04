# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from invitation.models import Event, Guest
from invitation.forms import EventForm
from django.utils import timezone
from invitation.forms import EventForm, GuestForm, GuestImportForm, DrinkOptionFormSet
from django.contrib import messages
from io import TextIOWrapper
import csv
from django.core.paginator import Paginator
from django.core.mail import send_mail
from .forms import ContactForm

@login_required
def dashboard_home(request):
    # 1. Récupérer tous les événements de l'utilisateur
    user_events = Event.objects.filter(organizer=request.user).order_by('-date')

    # 2. Calculer les statistiques globales
    total_events = user_events.count()
    
    # On filtre les invités liés aux événements de cet utilisateur
    base_guests = Guest.objects.filter(event__organizer=request.user)
    total_guests = base_guests.count()
    confirmed_guests = base_guests.filter(is_confirmed=True).count()
    
    # Calcul du pourcentage de confirmation (pour une barre de progression)
    confirmation_rate = 0
    if total_guests > 0:
        confirmation_rate = int((confirmed_guests / total_guests) * 100)

    # 3. Prochains événements (ex: les 3 prochains)
    upcoming_events = user_events.filter(date__gte=timezone.now())[:3]

    context = {
        'events': user_events,
        'total_events': total_events,
        'total_guests': total_guests,
        'confirmed_guests': confirmed_guests,
        'confirmation_rate': confirmation_rate,
        'upcoming_events': upcoming_events
    }
    
    return render(request, 'dashboard/index.html', context)

@login_required
def create_event(request):
    themes = [
        {'id': 'mariage_floral', 'name': 'Floral', 'img': 'img/themes/floral.jpg'},
        {'id': 'mariage_gold', 'name': 'Gold Luxury', 'img': 'img/themes/gold.jpg'},
        {'id': 'conf_tech', 'name': 'Tech Dark', 'img': 'img/themes/tech.jpg'},
        # ... etc
    ]
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('dashboard_home')
    else:
        form = EventForm()

    return render(request, 'dashboard/create_event.html', {'form': form, 'themes': themes})

@login_required
def manage_event(request, event_id):
    # Sécurité : On s'assure que l'événement appartient bien à l'utilisateur connecté
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    guests = event.guests.all().order_by('-id') # Les derniers ajoutés en premier

    paginator = Paginator(guests, 20) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    

    
    drink_stats = guests.filter(selected_drink__isnull=False)\
                        .values('selected_drink__name')\
                        .annotate(count=Count('selected_drink'))\
                        .order_by('-count')
    all_messages = event.guests.exclude(guestbook_message__exact='')\
                               .exclude(guestbook_message__isnull=True)\
                               .order_by('-responded_at')
    paginator_gb = Paginator(all_messages, 6)
    gb_page_number = request.GET.get('gb_page')
    guestbook_page_obj = paginator_gb.get_page(gb_page_number)

    guest_form = GuestForm()
    import_form = GuestImportForm()

    if request.method == 'POST':
        # CAS 1 : Ajout manuel d'un invité
        if 'add_guest' in request.POST:
            guest_form = GuestForm(request.POST)
            if guest_form.is_valid():
                guest = guest_form.save(commit=False)
                guest.event = event
                guest.save()
                messages.success(request, f"{guest.full_name} a été ajouté avec succès.")
                return redirect('manage_event', event_id=event.id)

        # CAS 2 : Import CSV
        elif 'import_csv' in request.POST:
            import_form = GuestImportForm(request.POST, request.FILES)
            if import_form.is_valid():
                csv_file = request.FILES['csv_file']
                # On lit le fichier en mode texte
                file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
                csv_reader = csv.reader(file_data)
                
                count = 0
                for row in csv_reader:
                    # On suppose format: Nom, Email (ignorer header si besoin)
                    if len(row) >= 2:
                        # Simple vérification pour éviter les en-têtes
                        if '@' in row[1]: 
                            Guest.objects.create(
                                event=event,
                                full_name=row[0].strip(),
                                email=row[1].strip()
                            )
                            count += 1
                
                messages.success(request, f"{count} invités importés avec succès !")
                return redirect('manage_event', event_id=event.id)

    context = {
        'event': event,
        'guest_form': guest_form,
        'import_form': import_form,
        'drink_stats': drink_stats,
        'page_obj': page_obj,
        'total_guests': paginator.count,
        'guestbook_page_obj': guestbook_page_obj,
    }
    return render(request, 'dashboard/manage_event.html', context)

@login_required # Sécurité : Seul l'organisateur (ou staff connecté) peut valider
def checkin_guest(request, uuid):
    guest = get_object_or_404(Guest, uuid=uuid)
    event = guest.event

    # Si on soumet le formulaire, c'est pour valider l'entrée
    if request.method == 'POST':
        if not guest.checked_in_at:
            guest.checked_in_at = timezone.now()
            guest.save()
            messages.success(request, f"Entrée validée pour {guest.full_name} !")
        else:
            messages.warning(request, "Cet invité est déjà entré.")
        
        # On recharge la page pour voir le nouveau statut
        return redirect('checkin_guest', uuid=uuid)

    return render(request, 'dashboard/checkin.html', {'guest': guest, 'event': event})

@login_required
def event_settings(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    if request.method == 'POST':
        # On charge le formulaire de l'event ET le formset des boissons
        form = EventForm(request.POST, request.FILES, instance=event)
        formset = DrinkOptionFormSet(request.POST, instance=event)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Paramètres et boissons mis à jour !")
            return redirect('event_settings', event_id=event.id)
    else:
        form = EventForm(instance=event)
        formset = DrinkOptionFormSet(instance=event)

    return render(request, 'dashboard/event_settings.html', {
        'event': event,
        'form': form,
        'formset': formset
    })

def landing_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Logique d'envoi d'email à l'admin
            # send_mail(...)
            messages.success(request, "Merci ! Nous avons bien reçu votre demande. Nous vous recontacterons sous 24h.")
            return redirect('landing_page')
    else:
        form = ContactForm()
    
    return render(request, 'landing.html', {'form': form})