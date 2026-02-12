from datetime import date, timedelta
from django.db import models
from django.db.models import Count


class CustomerRequest(models.Model):
    class SearchType(models.TextChoices):
        PRODUCT = 'product', 'Product Name'
        NUTRIENT = 'nutrient', 'Nutrient Type'
        CATEGORY = 'category', 'Category'

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='search_requests'
    )
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        related_name='search_requests'
    )
    search_type = models.CharField(
        max_length=20,
        choices=SearchType.choices
    )
    search_query = models.CharField(max_length=200)
    results_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.search_type}] '{self.search_query}' @ {self.store.name}"

    @classmethod
    def get_popular_searches(cls, store_id, days=30, limit=10):
        cutoff = date.today() - timedelta(days=days)
        return cls.objects.filter(
            store_id=store_id,
            created_at__gte=cutoff
        ).values('search_query', 'search_type').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]