from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from .constants import TRANSACTION_TYPE 

# Create your models here.
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Transactions')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)  # 'deposit', 'borrow', 'return'
    timestamp = models.DateTimeField(auto_now_add=True)
    returned = models.BooleanField(default=False)  
    
    def __str__(self):
        return f'{self.user.username} - {self.amount}'