from datetime import date, timedelta
from django.db.models import Count, Sum
from django.db.models.functions import TruncDate

from stores.models import Aisle
from inventory.models import StockItem
from inventory.services import ExpiryService
from .models import CustomerRequest


class AnalyticsService:
    @staticmethod
    def get_popular_products(store_id: int, days: int = 30):
        cutoff = date.today() - timedelta(days=days)
        return list(CustomerRequest.objects.filter(
            store_id=store_id,
            search_type='product',
            created_at__gte=cutoff
        ).values('search_query').annotate(
            count=Count('id')
        ).order_by('-count')[:10])

    @staticmethod
    def get_popular_nutrients(store_id: int, days: int = 30):
        cutoff = date.today() - timedelta(days=days)
        return list(CustomerRequest.objects.filter(
            store_id=store_id,
            search_type='nutrient',
            created_at__gte=cutoff
        ).values('search_query').annotate(
            count=Count('id')
        ).order_by('-count')[:10])

    @staticmethod
    def get_unfulfilled_searches(store_id: int, days: int = 7):
        cutoff = date.today() - timedelta(days=days)
        return list(CustomerRequest.objects.filter(
            store_id=store_id,
            results_count=0,
            created_at__gte=cutoff
        ).values('search_query', 'search_type').annotate(
            count=Count('id')
        ).order_by('-count')[:20])

    @staticmethod
    def get_daily_search_trends(store_id: int, days: int = 14):
        cutoff = date.today() - timedelta(days=days)
        return list(CustomerRequest.objects.filter(
            store_id=store_id,
            created_at__gte=cutoff
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            count=Count('id')
        ).order_by('date'))

    @staticmethod
    def get_dashboard_summary(store_id: int):
        # Stock alerts
        alerts = ExpiryService.get_stock_alerts(store_id)

        # Aisle overview
        aisles = Aisle.objects.filter(store_id=store_id).annotate(
            total_products=Count('stock_items__product', distinct=True),
            total_quantity=Sum('stock_items__quantity')
        )

        return {
            'stock_alerts': alerts,
            'aisle_overview': [
                {
                    'number': a.number,
                    'name': a.name,
                    'product_count': a.total_products or 0,
                    'total_items': a.total_quantity or 0,
                }
                for a in aisles
            ],
            'popular_products': AnalyticsService.get_popular_products(store_id, 7),
            'popular_nutrients': AnalyticsService.get_popular_nutrients(store_id, 7),
            'unfulfilled_searches': AnalyticsService.get_unfulfilled_searches(store_id, 7),
        }