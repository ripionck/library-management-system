from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib import messages
from django.views.generic import  DetailView, ListView
from .forms import ReviewForm
from .models import Book, Review
from users.models import UserProfile
from transactions.models import Transaction
        
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
    
class BorrowBookView(View):
    template_name = 'book_details.html'  
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        borrowing_price = book.borrowing_price

        user, created = UserProfile.objects.get_or_create(user=request.user)

        if user.balance >= borrowing_price:
            # Decrease user's balance
            user.balance -= borrowing_price
            user.save()

            # Add book to borrow history
            Transaction.objects.create(account=user, book=book, transaction_type='Borrow')

            messages.success(request, 'Book borrowed successfully.')
            return redirect('borrow_history')
        else:
            messages.error(request, 'Insufficient balance to borrow this book.')

        return HttpResponseBadRequest("Invalid request")

            
@method_decorator(login_required, name='dispatch')
class BorrowHistoryListView(ListView):
    template_name = 'books/borrow_history.html'
    model = Book
    

@login_required
def return_book(request, pk):
    transaction = Transaction.objects.get(pk=pk)

    if not transaction.returned and request.user.profile == transaction.user:
        # Mark the transaction as returned
        transaction.returned = True
        transaction.save()

        # Increase user's balance by the borrowed amount
        transaction.user.balance += transaction.amount
        transaction.user.save()

        messages.success(request, 'Book returned successfully.')
    else:
        messages.error(request, 'Invalid return request.')

    return redirect('borrow_history')



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