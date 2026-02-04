from django.template.loader import render_to_string
from weasyprint import HTML
import qrcode
from io import BytesIO

def generate_invitation_pdf(guest):
    # 1. Choisir le template HTML selon le type d'événement
    template_name = f"invitations/{guest.event.event_type.lower()}.html"
    
    # 2. Générer un QR Code pour l'invité (Optionnel)
    qr = qrcode.make(f"https://monsite.com/check-in/{guest.uuid}")
    qr_img = BytesIO()
    qr.save(qr_img, format='PNG')
    # (Il faudrait convertir qr_img en base64 pour l'afficher dans le HTML)

    # 3. Préparer le contexte
    context = {
        'guest': guest,
        'event': guest.event,
        # 'qr_code': qr_base64...
    }

    # 4. Rendu HTML
    html_string = render_to_string(template_name, context)

    # 5. Conversion en PDF
    pdf_file = HTML(string=html_string).write_pdf()
    
    return pdf_file