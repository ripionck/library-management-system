from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .constants import DEPOSIT
from .forms import DepositForm
from .email_utils import send_transaction_email

# Create your views here.
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