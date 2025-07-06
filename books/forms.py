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
        fields = ['title', 'author', 'magic_type', 'book_class', 'summary', 'zine_code']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'magic_type': forms.Select(),
            'book_class': forms.Select(),
            'summary': forms.Textarea(attrs={'placeholder': 'Describe the contents...', 'rows': 4}),
        }