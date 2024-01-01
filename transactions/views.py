from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Transaction
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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

