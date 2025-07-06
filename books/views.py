# books/views.py

from django.shortcuts import render, redirect
from .forms import BookForm

def home(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['zine_code'].strip()
            if code != GCL_SECRET_CODE:
                form.add_error('zine_code', 'Invalid GCL Zine Code.')
            else:
                form.save()
                return redirect("home")  # Or a thank-you page
    else:
        form = BookForm()
    return render(request, 'books/home.html', {"form": form})

def card(request):
    return render(request, 'books/card.html')