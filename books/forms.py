# books/forms.py

from django import forms
from .models import Book, Tag

class BookForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags and tags.count() > 10:
            raise forms.ValidationError("You can only select up to 10 tags.")
        return tags

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
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'type_code': forms.Select(),
            'class_code': forms.Select(),
            'summary': forms.Textarea(attrs={'placeholder': 'Describe the contents...', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        book = super().save(commit=False)
        if commit:
            book.save()
            self.save_m2m()
        return book