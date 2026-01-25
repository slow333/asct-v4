from django.forms import ModelForm
from .models import Book, BookInstance, Author
from django import forms

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'summary', 'isbn', 'author', 'genre', 'language' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
            'genre': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'language': forms.Select(attrs={'class': 'form-select'}),
        }
        help_texts = {
            'title': '책 제목을 입력해주세요.',
        }

class BookInstanceForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ('book', 'imprint', 'due_back', 'status', 'borrower')
        widgets = {
            'book': forms.Select(attrs={'class': 'form-select'}),
            'imprint': forms.TextInput(attrs={'class': 'form-control'}),
            'due_back': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'borrower': forms.Select(attrs={'class': 'form-select'}),
        }

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_of_death': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }