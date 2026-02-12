from django.urls import path
from .views import (
    StockListView, StockDetailView,
    ExpiringStockView, ExpiredStockView,
    LowStockView, StockAlertsView
)

urlpatterns = [
    path('', StockListView.as_view(), name='stock-list'),
    path('<int:pk>/', StockDetailView.as_view(), name='stock-detail'),
    path('expiring/', ExpiringStockView.as_view(), name='stock-expiring'),
    path('expired/', ExpiredStockView.as_view(), name='stock-expired'),
    path('low/', LowStockView.as_view(), name='stock-low'),
    path('alerts/', StockAlertsView.as_view(), name='stock-alerts'),
]