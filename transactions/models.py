from django.db import models
from users.models import UserProfile
from books.models import Book
from .constants import TRANSACTION_TYPE 

# Create your models here.
class Transaction(models.Model):
    account = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    balance_after_transaction = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)  
    timestamp = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)  
    
    def __str__(self):
        return f'{self.account} - {self.amount}'