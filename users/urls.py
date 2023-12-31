from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileUpdateView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('profile/', UserProfileUpdateView.as_view(), name='user_profile')
]
