from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest
from django.views import View
from transactions.constants import BORROW_BOOK
from django.contrib.auth.mixins import LoginRequiredMixin
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
    
@method_decorator(login_required, name='dispatch')
class BorrowBookView(View):
    template_name = 'books/book_details.html'  
    
    def post(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        borrowing_price = book.borrowing_price

        user, created = UserProfile.objects.get_or_create(user=request.user)

        if user.balance >= borrowing_price:
            # Decrease user's balance
            user.balance -= borrowing_price
            user.save()
            
            transaction = Transaction(
                        account=user,
                        amount=book.borrowing_price,
                        balance_after_transaction=user.balance,
                        transaction_type=BORROW_BOOK,
                        book=book
                    )
            transaction.save()

            messages.success(request, 'Book borrowed successfully.')
            return redirect('borrow_history')
        else:
            messages.error(request, 'Insufficient balance to borrow this book.')

        return HttpResponseBadRequest("Invalid request")


@method_decorator(login_required, name='dispatch')     
class BorrowHistoryView(View):
    template_name = 'books/borrow_history.html' 

    def get(self, request, *args, **kwargs):
        # Retrieve borrow book history transactions for the current user
        transactions = Transaction.objects.filter(account__user=request.user, transaction_type=BORROW_BOOK)

        # Pass the transactions to the template
        context = {'transactions': transactions}
        print(context)
        return render(request, self.template_name, context)
    
@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    def post(self, request, pk):
        # Get the transaction for the given primary key
        transaction = get_object_or_404(Transaction, pk=pk)
        print(transaction)

        # Check if the book has already been returned
        if transaction.returned:
            messages.error(request, 'This book has already been returned.')
            return redirect('borrow_history')

        # Check if transaction.amount and transaction.account are not None before using them
        if transaction.amount is not None and transaction.account is not None:
            # Update the transaction as returned
            transaction.returned = True
            transaction.save()

            # Update the book's borrowing status
            book = transaction.book
            if book is not None:
                book.is_borrowed = False
                book.save()

            # Update the user's balance
            user_profile = transaction.account
            user_profile.balance += transaction.amount
            user_profile.save()

            messages.success(request, 'Book returned successfully.')
        else:
            messages.error(request, 'Invalid return request: transaction amount or account is None.')

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
            

#  class ReturnBookView(LoginRequiredMixin, View):
    def get(self, request, id):
        book = Book.objects.get(pk=id)
        buyer = self.request.user.profile
        borrowed_book = Transaction.objects.get(profile=buyer, book=book, is_returned=False)
        print(borrowed_book.id)
        if not borrowed_book.is_returned:
            borrowed_book.is_returned = True
            borrowed_book.save()            
            buyer.balance += book.price
            buyer.save()
            messages.success(self.request, 'Return Successfull')
            book.quantity +=1
            book.save()
            transaction = Transaction(
                profile = buyer,
                amount = book.price,
                balance_after_transaction = buyer.balance,
                transaction_type = RETURN_BOOK,
                book = book,
                is_returned = True
            )
            transaction.save()
            return redirect('profile')
        else:
            messages.error(self.request, 'Already Returned')
            return redirect('profile')