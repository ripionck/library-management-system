from django.db import models
from django.contrib.auth.models import User
from .constants import  GENDER_TYPE, PROFESSION_TYPE

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

