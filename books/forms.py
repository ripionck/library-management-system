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
        labels = {
            'comment': 'Comments',
            'rating': 'Ratings',  
        }
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['rows'] = 5 
        self.fields['comment'].widget.attrs['cols'] = 70
        self.fields['comment'].widget.attrs['placeholder'] = 'Enter your comments'
        self.fields['rating'].help_text = ''
        self.fields['comment'].help_text = ''