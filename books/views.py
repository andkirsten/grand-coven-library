# books/views.py

from django.shortcuts import render, redirect
from .forms import BookForm
from .models import Book, Tag


def home(request):
    books = Book.objects.all().order_by('created_at')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = BookForm()
    return render(request, 'books/booklist.html', {'form': form, 'books': books})

def card(request):
    return render(request, 'books/card.html')

def about(request):
    return render(request, 'books/about.html')