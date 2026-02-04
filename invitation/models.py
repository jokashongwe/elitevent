from django.db import models
from django.contrib.auth.models import User
import uuid

THEME_CHOICES = [
    ('mariage_floral', 'Mariage Floral'),
    ('mariage_gold', 'Mariage Doré Luxury'),
    ('conf_tech', 'Conférence Tech (Dark)'),
    ('conf_minimal', 'Conférence Minimaliste'),
    ('anniv_fun', 'Anniversaire Coloré'),
    ('mariage_passion', 'Mariage Passion'),
    ('mariage_pastel_hearts', 'Mariage Pastel')
]

class Event(models.Model):
    TYPE_CHOICES = [
        ('MARIAGE', 'Mariage'),
        ('CONFERENCE', 'Conférence'),
        ('ANNIVERSAIRE', 'Anniversaire'),
    ]
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    # L'image de fond ou le style choisi
    theme_template = models.CharField(max_length=50, choices=THEME_CHOICES, default='mariage_floral') 

    def get_template_path(self):
        """Retourne le chemin réel du fichier HTML"""
        return f"invitation/{self.theme_template}.html"

    def __str__(self):
        return self.title
    
class DrinkOption(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='drink_options')
    name = models.CharField(max_length=100) # ex: "Vin Rouge", "Champagne", "Jus de fruits"
    description = models.CharField(max_length=200, blank=True) # ex: "Château Margaux 2015"

    def __str__(self):
        return self.name

class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='guests')
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.TextField(max_length=20, blank=True)
    has_whatsapp = models.BooleanField(default=True)
    # Identifiant unique pour le lien de l'invitation ou le QR Code
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    selected_drink = models.ForeignKey(DrinkOption, on_delete=models.SET_NULL, null=True, blank=True)
    guestbook_message = models.TextField(blank=True, help_text="Message pour le livre d'or")
    
    # Date de réponse
    responded_at = models.DateTimeField(null=True, blank=True)

    @property
    def has_arrived(self):
        return self.checked_in_at is not None

    def __str__(self):
        return f"{self.full_name} - {self.event.title}"

