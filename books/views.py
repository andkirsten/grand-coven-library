# books/views.py

from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book, Tag
from django.conf import settings


def home(request):
    books = Book.objects.all().order_by('created_at')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['gcl_secret_code'].strip()
            if code != settings.GCL_SECRET_CODE:
                form.add_error('gcl_secret_code', 'Invalid GCL Password. Correct password can be found on page 14 of the GCL Zine.')
            else:
                form.save()
                return redirect("home")
    else:
        form = BookForm()
    return render(request, 'books/booklist.html', {'form': form, 'books': books})

def card(request):
    return render(request, 'books/card.html')

def about(request):
    return render(request, 'books/about.html')