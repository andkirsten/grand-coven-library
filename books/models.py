from django.db import models

from .utils import generate_call_number, generate_call_number_from_id

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
    ('ENC', 'Enchantments'), ('AST', 'Astrology'),
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
    author_first_name = models.CharField(max_length=40, blank=True)
    author_last_name = models.CharField(max_length=40, blank=True)
    magic_category= models.CharField(max_length=2, choices=MAGIC_CHOICES)
    book_type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    call_number = models.CharField(max_length=50, blank=True)
    summary = models.TextField(blank=True, max_length=1000)
    publisher = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)
    year = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True)
    entry_number = models.IntegerField(default=0, blank=True)
    notes = models.TextField(blank=True, max_length=1000)
    librarian = models.CharField(max_length=300, blank=True)

    def save(self, *args, **kwargs):
        # First save to get the ID
        super().save(*args, **kwargs)
        
        # If no call number exists, generate it using the ID as entry number
        if not self.call_number:
            self.entry_number = self.id
            self.call_number = generate_call_number_from_id(self)
            # Save again to update call_number and entry_number
            super().save(update_fields=['call_number', 'entry_number'])

    def __str__(self):
        return f"{self.title} ({self.call_number})"

    @property
    def call_number_parts(self):
        """Returns the call number split into three parts at the dots."""
        if self.call_number:
            return [part.strip() for part in self.call_number.split('.')]
        return []

    @property
    def call_number_magic(self):
        # Returns the first portion (e.g., 'DA-GRM')
        return self.call_number_parts[0] if len(self.call_number_parts) > 0 else ''

    @property
    def call_number_author(self):
        return self.call_number_parts[1] if len(self.call_number_parts) > 1 else ''

    @property
    def call_number_entry(self):
        return self.call_number_parts[2] if len(self.call_number_parts) > 2 else ''

    @property
    def author_display(self):
        if self.author_first_name or self.author_last_name:
            return f"{self.author_first_name} {self.author_last_name}".strip()
        return "Unknown"
