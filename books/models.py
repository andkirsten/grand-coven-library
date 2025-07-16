from django.db import models

from .utils import generate_call_number

TYPE_CHOICES = [
    ('Da', 'Dark'),
    ('Fo', 'Folk'),
    ('Na', 'Nature'),
    ('El', 'Elder'),
]

CLASS_CHOICES = [
    ('GRM', 'Grimoire'), ('FLD', 'Field Guide'), ('ESO', 'Esoterica'),
    ('BST', 'Bestiary'), ('RTL', 'Rituals'), ('PTN', 'Potions'),
    ('MKN', 'Machines'), ('RNS', 'Runes'), ('SMN', 'Summoning'),
    ('CRM', 'Charms and Enchantments'), ('AST', 'Astrology'),
    ('DVN', 'Divination'), ('HRB', 'Herbarium'), ('PRL', 'Portal Book'),

]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    type_code = models.CharField(max_length=2, choices=TYPE_CHOICES)
    class_code = models.CharField(max_length=3, choices=CLASS_CHOICES)
    call_number = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.call_number:
            self.call_number, self.entry_number = generate_call_number(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.call_number})"
