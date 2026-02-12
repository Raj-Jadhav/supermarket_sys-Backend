from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.permissions import IsStaffUser
from .services import AnalyticsService


class DashboardView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        summary = AnalyticsService.get_dashboard_summary(store_id)
        return Response(summary)


class PopularSearchesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        days = int(request.query_params.get('days', 30))
        return Response({
            'products': AnalyticsService.get_popular_products(store_id, days),
            'nutrients': AnalyticsService.get_popular_nutrients(store_id, days),
        })


class UnfulfilledSearchesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        days = int(request.query_params.get('days', 7))
        return Response(
            AnalyticsService.get_unfulfilled_searches(store_id, days)
        )


class SearchTrendsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        days = int(request.query_params.get('days', 14))
        return Response(
            AnalyticsService.get_daily_search_trends(store_id, days)
        )