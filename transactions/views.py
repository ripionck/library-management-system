from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Transaction
from decimal import Decimal
from django.urls import reverse_lazy
from .constants import DEPOSIT
from .forms import DepositForm
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
class DepositView(LoginRequiredMixin, CreateView):
    template_name = 'deposit_money.html'
    form_class = DepositForm
    success_url = reverse_lazy('user_profile')
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.profile
        account.balance += amount
        account.save(
            update_fields=[
                'balance'
            ]
        )
        transaction_obj = form.save(commit=False)
        transaction_obj.account = account
        transaction_obj.transaction_type = DEPOSIT
        transaction_obj.balance_after_transaction = account.balance
        transaction_obj.save()
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        send_transaction_email(self.request.user, amount,
                               "Deposite Message", "deposit_email.html")
        return super().form_valid(form)