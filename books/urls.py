# books/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('card/', views.card, name='card'),
    path('about/', views.about, name='about'),
]
