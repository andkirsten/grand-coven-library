
def generate_call_number(book_instance):
    from .models import Book
    last = (book_instance.author_last_name or '').strip()
    first = (book_instance.author_first_name or '').strip()
    author_code = (last[:2] or first[:2]).upper() if (last or first) else 'XX'

    last_entry = Book.objects.filter(
        magic_category=book_instance.magic_category,
        book_type=book_instance.book_type
    ).order_by('-entry_number').first()

    next_entry = 1 if not last_entry else last_entry.entry_number + 1
    entry_str = f"{next_entry:03d}"

    return f"{book_instance.book_type}-{book_instance.magic_category} . {author_code} . {entry_str}", next_entry
