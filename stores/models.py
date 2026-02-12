from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    manager = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_stores'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Aisle(models.Model):
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='aisles'
    )
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    allowed_categories = models.ManyToManyField(
        'products.Category',
        related_name='allowed_aisles',
        blank=True
    )

    class Meta:
        unique_together = ['store', 'number']
        ordering = ['number']

    def __str__(self):
        return f"Aisle {self.number} - {self.name} ({self.store.name})"

    def accepts_product(self, product):
        """Check if product categories intersect with aisle's allowed categories."""
        product_cats = set(product.categories.values_list('id', flat=True))
        allowed_cats = set(self.allowed_categories.values_list('id', flat=True))
        if not allowed_cats:
            return True  # If no restrictions, accept all
        return bool(product_cats & allowed_cats)