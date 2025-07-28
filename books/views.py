# books/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from .models import Book, Tag  
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib import messages
import weasyprint
from django.db.models import Q


def handle_book_form_submission(request):
    """Handle book form submission and return (success, form, show_modal)"""
    form = BookForm(request.POST)
    show_modal = False
    
    if form.is_valid():
        code = form.cleaned_data['gcl_secret_code'].strip()
        if code != settings.GCL_SECRET_CODE:
            form.add_error('gcl_secret_code', 'Invalid GCL Secret Code.')
            show_modal = True
        else:
            book = form.save(commit=False)
            # Handle tags
            tag_names = request.POST.getlist('tags')
            tag_objs = []
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tag_objs.append(tag)
            book.save()
            book.tags.set(tag_objs)
            form.save_m2m()
            return True, form, show_modal
    else:
        show_modal = True
    
    return False, form, show_modal


def home(request):
    books = Book.objects.all().order_by('created_at')
    show_modal = False
    
    # Handle search and filtering
    q = request.GET.get('q')
    magic_category = request.GET.get('magic_category')
    book_type = request.GET.get('book_type')
    
    print(f"Search query: {q}")
    print(f"Magic category: {magic_category}")
    print(f"Book type: {book_type}")
    
    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(author_first_name__icontains=q) |
            Q(author_last_name__icontains=q) |
            Q(summary__icontains=q) |
            Q(publisher__icontains=q) |
            Q(city__icontains=q) |
            Q(year__icontains=q) |
            Q(notes__icontains=q) |
            Q(tags__name__icontains=q)  # Also search in tags
        ).distinct()  # Use distinct to avoid duplicates from tag searches
    if magic_category:
        books = books.filter(magic_category=magic_category)
    if book_type:
        books = books.filter(book_type=book_type)
    
    if request.method == "POST":
        success, form, show_modal = handle_book_form_submission(request)
        if success:
            return redirect("home")
    else:
        form = BookForm()
    
    return render(request, 'books/booklist.html', {'form': form, 'books': books, 'show_modal': show_modal})

def card(request):
    return render(request, 'books/card.html')

def about(request):
    form = BookForm()
    
    if request.method == "POST":
        # Check if this is a book form submission (from modal)
        if 'title' in request.POST:
            success, form, _ = handle_book_form_submission(request)
            if success:
                return redirect("home")
        else:
            # Handle contact form submission
            email = request.POST.get('email')
            call_number = request.POST.get('call_number')
            message = request.POST.get('message')
            
            if email and call_number and message:
                # Send email
                subject = f"GCL Contact Form - Call Number: {call_number}"
                email_message = f"""
New contact form submission from the Grand Coven Library:

Email: {email}
Call Number: {call_number}
Message: {message}

---
This message was sent from the GCL contact form.
                """
                
                try:
                    # Send to your email
                    send_mail(
                        subject=subject,
                        message=email_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.ADMIN_EMAIL],
                        fail_silently=False,
                    )
                    messages.success(request, "Your message has been sent successfully!")
                except Exception as e:
                    messages.error(request, "Sorry, there was an error sending your message. Please try again or contact us directly.")
                    print(f"Email error: {e}")
            else:
                messages.error(request, "Please fill in all required fields.")
            
            # Redirect to prevent form resubmission on refresh
            return redirect('about')
    
    return render(request, 'books/about.html', {'form': form})

def print_card(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    html = render_to_string('books/print_card.html', {'book': book})
    pdf = weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=\"catalog_card_{book.id}.pdf\"'
    return response

@property
def call_number_magic(self):
    return self.call_number_parts[0] if len(self.call_number_parts) > 0 else ''

@property
def call_number_author(self):
    return self.call_number_parts[1] if len(self.call_number_parts) > 1 else ''

@property
def call_number_entry(self):
    return self.call_number_parts[2] if len(self.call_number_parts) > 2 else ''

def card_preview(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'books/print_card.html', {'book': book})