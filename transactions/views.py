from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .models import Transaction
from decimal import Decimal
from django.db.models import F
from books.models import Book
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from books.models import Review
from users.models import UserProfile

# Create your views here.
def send_transaction_email(user, amount, subject, template):
    message = render_to_string(template, {
        'user': user,
        'amount': amount,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()
        

# Write your views here
def deposit_money(request):
    if request.method == 'POST':
        amount_str = request.POST.get('amount')
        if amount_str:
            # Convert the string amount to Decimal
            amount = Decimal(amount_str)
            
            # Get the UserProfile instance
            user = UserProfile.objects.get(user=request.user)
            print(user)
            
            # Update the balance in the UserProfile
            user.balance += amount
            user.save()

            # Use the associated User instance for the Transaction
            Transaction.objects.create(account=user, amount=amount, transaction_type='Deposit')

            send_transaction_email(request.user, amount,
                               "Deposite Message", "deposit_email.html")
            
            # Send email here (use Django's EmailMessage)
            messages.success(request, 'Deposit successful.')
            return redirect('user_profile')

    return render(request, 'deposit_money.html')

@login_required
def borrow_book(request, pk):
    book = Book.objects.get(pk=pk)

    if request.method == 'POST':
        borrowing_price = book.borrowing_price
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        print(user_profile.balance)

        if user_profile.balance >= borrowing_price:
            # Decrease user's balance
            user_profile.balance -= borrowing_price
            user_profile.save()
            print(user_profile.balance)
            

            # Add book to borrow history
            Transaction.objects.create(user=user_profile.user, book=book, transaction_type='Borrow')

            messages.success(request, 'Book borrowed successfully.')
            return redirect('borrow_history')
        else:
            messages.error(request, 'Insufficient balance to borrow this book.')
            
    return HttpResponseBadRequest("Invalid request")

            
@login_required
def borrow_history(request):
    template_name = 'borrowing_history.html'
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=user_profile.user, transaction_type='Borrow')
    return render(request, template_name, {'transactions': transactions})

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

def user_profile(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user)
    reviews = Review.objects.filter(user=user)
    return render(request, 'user_profile.html', {'user': user, 'transactions': transactions, 'reviews': reviews})
