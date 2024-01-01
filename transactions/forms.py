from django import forms
from .models import Transaction

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['amount', 'transaction_type']

#     def __init__(self, *args, **kwargs):
#         # Pop 'user' value from keyword arguments
#         self.user_instance = kwargs.pop('user_instance')
#         super().__init__(*args, **kwargs)
#         # Disable the 'transaction_type' field
#         self.fields['transaction_type'].disabled = True
#         # Hide the 'transaction_type' field in the form
#         self.fields['transaction_type'].widget = forms.HiddenInput()

#     def save(self, commit=True):
#         # Set the 'user' field before saving
#         self.instance.user = self.user_instance
#         return super().save(commit)
class DepositForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        fields = ['amount']
        def clean_amount(self):
            min_deposit_amount = 100
            amount = self.cleaned_data.get('amount')
            if amount < min_deposit_amount:
                raise forms.ValidationError(
                    f'You need to deposit at least {min_deposit_amount} $'
                )

            return amount