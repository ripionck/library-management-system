from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from .constants import RATING_CHOICES, GENDER_TYPE, PROFESSION_TYPE

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_TYPE)
    profession = models.CharField(max_length=100, choices=PROFESSION_TYPE)
    phone_number = models.CharField(max_length=12)
    address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.comment
