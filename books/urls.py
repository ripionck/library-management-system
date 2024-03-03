from django.urls import path
from .views import BookDetailsView, BookListView, CreateReviewView, BorrowBookView, BorrowHistoryView, ReturnBookView

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
    path('details/<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('borrow/<int:pk>/', BorrowBookView.as_view(), name='borrow_book'),
    path('borrow/history/', BorrowHistoryView.as_view(), name='borrow_history'),
    path('borrow/return/<int:pk>/', ReturnBookView.as_view(), name='return_book'),
    path('review/<int:book_id>/', CreateReviewView.as_view(), name='book_review')
]
