# books/forms.py

from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    zine_code = forms.CharField(
        max_length=100,
        required=True,
        label="GCL Zine Code",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your secret code...',
        })
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'type_code', 'class_code', 'summary', 'zine_code']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'type_code': forms.Select(),
            'class_code': forms.Select(),
            'summary': forms.Textarea(attrs={'placeholder': 'Describe the contents...', 'rows': 4}),
        }