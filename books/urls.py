from django.urls import path
from .views import BookDetailsView, BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailsView.as_view(), name='book_details'),
]
