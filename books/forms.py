from django import forms
from .models import Book, Review

class AddBookForm(forms.ModelForm):
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publisher', 'borrowing_price', 'date_of_publication', 'description', 'image', 'categories']
        widgets = {
            'categories' : forms.CheckboxSelectMultiple
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
