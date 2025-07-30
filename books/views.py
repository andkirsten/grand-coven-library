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
    print("=== FORM SUBMISSION DEBUG ===")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    
    form = BookForm(request.POST)
    print(f"Form is valid: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"Form errors: {form.errors}")
        print(f"Form non-field errors: {form.non_field_errors()}")
    
    show_modal = False
    
    if form.is_valid():
        code = form.cleaned_data['gcl_secret_code'].strip()
        print(f"Secret code entered: '{code}'")
        print(f"Expected code: '{settings.GCL_SECRET_CODE}'")
        
        if code != settings.GCL_SECRET_CODE:
            print("Secret code mismatch!")
            form.add_error('gcl_secret_code', 'Invalid GCL Secret Code.')
            show_modal = True
        else:
            print("Secret code correct, saving book...")
            book = form.save(commit=False)
            print(f"Book object created: {book}")
            book.save()
            print(f"Book saved with ID: {book.id}")
            
            # Handle tags - create new tags if they don't exist
            tags_string = form.cleaned_data.get('tags', '')
            print(f"Tags string from form: '{tags_string}'")
            
            tag_objects = []
            if tags_string:
                # Split by comma and process each tag
                tag_names = [name.strip() for name in tags_string.split(',') if name.strip()]
                print(f"Tag names to process: {tag_names}")
                
                for tag_name in tag_names:
                    if tag_name:  # Only process non-empty tags
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        tag_objects.append(tag)
                        if created:
                            print(f"Created new tag: '{tag_name}'")
                        else:
                            print(f"Found existing tag: '{tag_name}'")
            
            # Set the tags on the book
            book.tags.set(tag_objects)
            print(f"Set {len(tag_objects)} tags on book")
            
            return True, form, show_modal
    else:
        show_modal = True
    
    return False, form, show_modal


def home(request):
    books = Book.objects.all().order_by('-created_at') 
    show_modal = False
    
    # Handle search and filtering
    q = request.GET.get('q')
    magic_category = request.GET.get('magic_category')
    book_type = request.GET.get('book_type')
    
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
            Q(tags__name__icontains=q)  
        ).distinct()  
    if magic_category:
        books = books.filter(magic_category=magic_category)
    if book_type:
        books = books.filter(book_type=book_type)
    
    if request.method == "POST":
        print("=== HOME VIEW: POST request received ===")
        success, form, show_modal = handle_book_form_submission(request)
        print(f"Form submission result: success={success}, show_modal={show_modal}")
        if success:
            print("Redirecting to home...")
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
    
    try:
        print(f"Generating PDF for book {book_id}")
        print(f"Base URL: {request.build_absolute_uri()}")
        
        # Add timeout and better error handling for WeasyPrint
        pdf = weasyprint.HTML(
            string=html, 
            base_url=request.build_absolute_uri()
        ).write_pdf(
            optimize_images=True,
            jpeg_quality=85
        )
        print("PDF generated successfully")
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=\"catalog_card_{book.id}.pdf\"'
        return response
    except Exception as e:
        print(f"PDF generation error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        # Fallback to HTML preview
        return render(request, 'books/print_card.html', {'book': book})

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