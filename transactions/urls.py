from django.urls import path
from .views import deposit_money

urlpatterns = [
    path('deposit/', deposit_money, name='deposit_money')
]