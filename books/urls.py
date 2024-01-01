from django.urls import path
from .views import BookDetailsView, BookListView, CreateReviewView,BorrowBookView ,BorrowHistoryListView, return_book

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('borrow/<int:pk>/', BorrowBookView.as_view(), name='borrow_book'),
    path('borrow/history/', BorrowHistoryListView.as_view(), name='borrow_history'),
    path('borrow/return/<int:pk>/', return_book, name='return_book'),
    path('review/<int:book_id>/', CreateReviewView.as_view(), name='book_review')
]
