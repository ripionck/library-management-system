from django.urls import path
from .views import BookDetailsView, BookListView, CreateReviewView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailsView.as_view(), name='book_details'),
    path('review/<int:book_id>/', CreateReviewView.as_view(), name='book_review')
]
