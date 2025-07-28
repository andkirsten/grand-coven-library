from .models import MAGIC_CHOICES, TYPE_CHOICES

def book_choices(request):
    return {
        'magic_choices': MAGIC_CHOICES,
        'type_choices': TYPE_CHOICES,
    }
