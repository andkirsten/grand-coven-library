




def generate_call_number(book_instance):
    from .models import Book
    if book_instance.author:
        parts = book_instance.author.strip().split()
        author_code = parts[-1][:2].upper() if len(parts) > 1 else parts[0][:2].upper()
    else:
        title_words = [w for w in book_instance.title.split() if w.lower() not in ['a', 'an', 'the']]
        author_code = title_words[0][:2].upper() if title_words else 'XX'

    last_entry = Book.objects.filter(
        type_code=book_instance.type_code,
        class_code=book_instance.class_code
    ).order_by('-entry_number').first()

    next_entry = 1 if not last_entry else last_entry.entry_number + 1
    entry_str = f"{next_entry:03d}"

    return f"{book_instance.type_code}-{book_instance.class_code} . {author_code} . {entry_str}", next_entry
