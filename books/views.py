from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import  DetailView
from .forms import ReviewForm
from .models import Book, Review
from users.models import UserProfile
        
# Create your views here.    
class BookListView(View):
    template_name = 'books/book_list.html'

    def get(self, request):
        books = Book.objects.all()
        return render(request, self.template_name, {'books': books})
    
class BookDetailsView(DetailView):
    model = Book
    template_name = 'books/book_details.html'
    context_object_name = 'book'

@method_decorator(login_required, name='dispatch')
class CreateReviewView(View):
    template_name = 'books/create_review.html'

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = ReviewForm()
        return render(request, self.template_name, {'book': book, 'form': form})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Get the UserProfile instance corresponding to the logged-in user
            user_profile = get_object_or_404(UserProfile, user=request.user)

            Review.objects.create(user=user_profile, book=book, rating=rating, comment=comment)

            # You may want to add a success message or redirect to the book detail page
            return redirect('book_review', book_id=book.id)

        # If form is not valid, render the form again with errors
        return render(request, self.template_name, {'book': book, 'form': form})