from django.urls import path
# from .views import deposit_money
from .views import DepositView

urlpatterns = [
    # path('deposit/', deposit_money, name='deposit_money')
     path('deposit/', DepositView.as_view(), name='deposit_money')
]