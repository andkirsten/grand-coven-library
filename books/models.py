from django.db import models

# books/models.py

from django.db import models

TYPE_CHOICES = [
    ('Da', 'Dark'),
    ('Fo', 'Folk'),
    ('Na', 'Nature'),
    ('El', 'Elder'),
]

CLASS_CHOICES = [
    ('01', 'Grimoire'),
    ('02', 'Field Guide'),
    ('03', 'Esoterica'),
    ('04', 'Bestiary'),
    ('05', 'Rituals'),
    ('06', 'Potions'),
    ('07', 'Machines'),
    ('08', 'Runes'),
    ('09', 'Summoning'),
    ('10', 'Charms and Enchantments'),
    ('11', 'Astrology'),
    ('12', 'Divination'),
    ('13', 'Herbarium'),
    ('14', 'Portal Book'),
]

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    magic_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    book_class = models.CharField(max_length=2, choices=CLASS_CHOICES)
    summary = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def get_entry_number(self):
        return f"{self.id:03}" if self.id else "000"

    def get_author_code(self):
        return self.author.strip().split()[-1][:2].capitalize() if self.author else "??"

    @property
    def call_number(self):
        return f"{self.magic_type} {self.book_class}.{self.get_entry_number()} {self.get_author_code()}"

    def __str__(self):
        return f"{self.title} ({self.call_number})"

