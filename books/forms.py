from django import forms
from .models import Book, Category

class AddBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'borrowing_price', 'date_of_publication', 'description', 'image', 'categories']
        widgets = {
            'categories' : forms.CheckboxSelectMultiple
        }