from django.contrib import admin
from .models import UserProfile, Review

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Review)