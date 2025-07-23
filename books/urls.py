# books/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('card/', views.card, name='card'),
    path('about/', views.about, name='about'),
    path('books/<int:book_id>/print_card/', views.print_card, name='print_card'),
]
