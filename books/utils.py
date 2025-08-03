
def generate_call_number(book_instance):
    from .models import Book
    last = (book_instance.author_last_name or '').strip()
    first = (book_instance.author_first_name or '').strip()
    
    # If author is anonymous or no author name provided, use first two letters of title
    if book_instance.author_anonymous or not (last or first):
        author_code = book_instance.title[:2].upper() if book_instance.title else 'XX'
    else:
        author_code = (last[:2] or first[:2]).upper()

    last_entry = Book.objects.filter(
        magic_category=book_instance.magic_category,
        book_type=book_instance.book_type
    ).order_by('-entry_number').first()

    next_entry = 1 if not last_entry else last_entry.entry_number + 1
    entry_str = f"{next_entry:03d}"

    return f"{book_instance.magic_category}-{book_instance.book_type} . {author_code} . {entry_str}", next_entry

def generate_call_number_from_id(book_instance):
    """Generate call number using the book's ID as the entry number"""
    last = (book_instance.author_last_name or '').strip()
    first = (book_instance.author_first_name or '').strip()
    
    # If author is anonymous or no author name provided, use first two letters of title
    if book_instance.author_anonymous or not (last or first):
        author_code = book_instance.title[:2].upper() if book_instance.title else 'XX'
    else:
        author_code = (last[:2] or first[:2]).upper()
    
    entry_str = f"{book_instance.id:03d}"
    
    return f"{book_instance.magic_category}-{book_instance.book_type} . {author_code} . {entry_str}"
