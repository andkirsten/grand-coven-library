from django.db import models

from .utils import generate_call_number

MAGIC_CHOICES = [
    ('DA', 'Dark'),
    ('FO', 'Folk'),
    ('NA', 'Nature'),
    ('EL', 'Elder'),
]

TYPE_CHOICES = [
    ('GRM', 'Grimoire'), ('FLD', 'Field Guide'), ('ESO', 'Esoterica'),
    ('BST', 'Bestiary'), ('RTL', 'Rituals'), ('PTN', 'Potions'),
    ('MKN', 'Machines'), ('RNS', 'Runes'), ('SMN', 'Summoning'),
    ('CRM', 'Charms and Enchantments'), ('AST', 'Astrology'),
    ('DVN', 'Divination'), ('HRB', 'Herbarium'), ('PRL', 'Portal Book'),

]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_suggested = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=1000)
    author_anonymous = models.BooleanField(default=False, blank=True)
    author_first_name = models.CharField(max_length=200, blank=True)
    author_last_name = models.CharField(max_length=200, blank=True)
    magic_category= models.CharField(max_length=2, choices=MAGIC_CHOICES)
    book_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    call_number = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True)
    publisher = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    entry_number = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    librarian = models.CharField(max_length=300, blank=True)

    def save(self, *args, **kwargs):
        if not self.call_number:
            self.call_number, self.entry_number = generate_call_number(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.call_number})"
