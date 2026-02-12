from django.urls import path
from .views import (
    DashboardView, PopularSearchesView,
    UnfulfilledSearchesView, SearchTrendsView
)

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('popular/', PopularSearchesView.as_view(), name='popular-searches'),
    path('unfulfilled/', UnfulfilledSearchesView.as_view(), name='unfulfilled-searches'),
    path('trends/', SearchTrendsView.as_view(), name='search-trends'),
]