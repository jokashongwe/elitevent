import qrcode
import base64
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from .models import Guest, DrinkOption
from django.utils import timezone


def view_invitation(request, uuid):
    # On récupère l'invité grâce à son UUID unique (impossible à deviner)
    guest = get_object_or_404(Guest, uuid=uuid)
    event = guest.event
    
    # --- Génération du QR Code ---
    # Le QR Code pointe vers l'URL de validation (pour le jour J)
    # Ici, on simule une URL de check-in
    checkin_url = request.build_absolute_uri(f'/checkin/{uuid}/')
    
    qr = qrcode.make(checkin_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    # On convertit l'image en chaîne de caractères base64 pour l'injecter dans le HTML
    img_str = base64.b64encode(buffer.getvalue()).decode()
    qr_code_data = f"data:image/png;base64,{img_str}"

    # Si l'invité envoie sa réponse
    if request.method == 'POST':
        # 1. Récupérer le message
        message = request.POST.get('guestbook_message')
        
        # 2. Récupérer la boisson choisie (ID)
        drink_id = request.POST.get('selected_drink')
        
        # 3. Mettre à jour l'invité
        guest.guestbook_message = message
        if drink_id:
            guest.selected_drink = get_object_or_404(DrinkOption, id=drink_id)
        
        guest.is_confirmed = True
        guest.responded_at = timezone.now()
        guest.save()
        
        # Redirection vers la même page avec un paramètre de succès (pour afficher un merci)
        return redirect(f"{request.path}?confirmed=true")
    
    drink_options = event.drink_options.all()

    context = {
        'guest': guest,
        'event': event,
        'qr_code_url': qr_code_data,
        'drink_options': drink_options,
        'is_success': request.GET.get('confirmed') == 'true'
    }
    
    # Sélection du bon template selon le type d'événement
    try:
        return render(request, event.get_template_path(), context)
    except:
        return render(request, 'invitation/default.html', context)