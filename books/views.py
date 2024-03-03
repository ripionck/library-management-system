from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseBadRequest
from django.views import View
from transactions.constants import BORROW_BOOK
from django.contrib import messages
from django.views.generic import DetailView
from .forms import ReviewForm
from .models import Book, Review, Category
from users.models import UserProfile
from transactions.models import Transaction
from transactions.email_utils import send_transaction_email


# Create your views here.
class BookListView(View):
    template_name = 'books/book_list.html'

    def get(self, request, *args, **kwargs):
        category_name = request.GET.get('category_name')

        if category_name:
            books = Book.objects.filter(category__name=category_name)
            print(books)
        else:
            books = Book.objects.all()

        categories = Category.objects.all()  # Assuming you have a Category model

        return render(request, self.template_name, {'books': books, 'categories': categories})


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
        # Check if the user has already borrowed the same book and it's not returned
        existing_borrow_book = Transaction.objects.filter(
            account=user, book=book, is_returned=False).first()

        if existing_borrow_book:
            messages.error(
                self.request, 'You have already borrowed this book. You cannot borrow the same book twice at the same time.')
            return redirect('book_details', pk=pk)
        else:
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
                send_transaction_email(self.request.user, transaction.amount,
                                       "Borrow Book Message", "books/borrow_book_email.html")
                return redirect('borrow_history')
            else:
                messages.error(
                    request, 'Insufficient balance to borrow this book.')

        return HttpResponseBadRequest("Invalid request")


@method_decorator(login_required, name='dispatch')
class BorrowHistoryView(View):
    template_name = 'books/borrow_history.html'

    def get(self, request, *args, **kwargs):
        # Retrieve borrow book history transactions for the current user
        transactions = Transaction.objects.filter(
            account__user=request.user, transaction_type=BORROW_BOOK)

        # Pass the transactions to the template
        context = {'transactions': transactions}
        print(context)
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    def post(self, request, pk):
        # Get the transaction for the given primary key
        transaction = get_object_or_404(Transaction, pk=pk)

        # Check if the book has already been returned
        if transaction.is_returned:
            messages.error(request, 'This book has already been returned.')
            return redirect('borrow_history')

        # Check if transaction.amount and transaction.account are not None before using them
        if transaction.amount is not None and transaction.account is not None:
            # Update the transaction as returned
            transaction.is_returned = True
            transaction.save()

            # Update the user's balance
            account = transaction.account
            account.balance += transaction.amount
            account.save()
            print(account)

            messages.success(request, 'Book returned successfully.')
            send_transaction_email(self.request.user, transaction.amount,
                                   "Return Book Message", "books/return_book_email.html")
        else:
            messages.error(
                request, 'Invalid return request: transaction amount or account is None.')

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

            Review.objects.create(
                user=user_profile, book=book, rating=rating, comment=comment)

            return redirect('book_review', book_id=book.id)

        # If form is not valid, render the form again with errors
        return render(request, self.template_name, {'book': book, 'form': form})
