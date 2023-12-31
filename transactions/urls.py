from django.urls import path
from .views import deposit_money, borrow_book, return_book, borrow_history

urlpatterns = [
    path('deposit/', deposit_money, name='deposit_money'),
    path('borrow/<int:pk>/', borrow_book, name='borrow_book'),
    path('borrow/history/', borrow_history, name='borrow_history'),
    path('borrow/return/<int:pk>/', return_book, name='return_book'),
]