from datetime import date, timedelta
from django.db import models
from django.core.exceptions import ValidationError


class StockItem(models.Model):
    class ExpiryStatus(models.TextChoices):
        SAFE = 'safe', 'Safe'
        EXPIRING_SOON = 'expiring', 'Expiring Soon'
        EXPIRED = 'expired', 'Expired'

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='stock_items'
    )
    aisle = models.ForeignKey(
        'stores.Aisle',
        on_delete=models.CASCADE,
        related_name='stock_items'
    )
    quantity = models.PositiveIntegerField(default=0)
    stocked_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    batch_number = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['expiry_date']

    def __str__(self):
        return f"{self.product.name} @ Aisle {self.aisle.number} (qty: {self.quantity})"

    def clean(self):
        """BUSINESS LOGIC: Validate aisle accepts this product's categories."""
        if self.aisle_id and self.product_id:
            if not self.aisle.accepts_product(self.product):
                allowed = list(self.aisle.allowed_categories.values_list('name', flat=True))
                product_cats = list(self.product.categories.values_list('name', flat=True))
                raise ValidationError(
                    f"Product categories {product_cats} don't match "
                    f"aisle allowed categories {allowed}. "
                    f"Cannot place '{self.product.name}' in '{self.aisle.name}'."
                )

    def save(self, *args, **kwargs):
        if not self.expiry_date:
            self.expiry_date = date.today() + timedelta(
                days=self.product.shelf_life_days
            )
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def expiry_status(self) -> str:
        today = date.today()
        days_left = (self.expiry_date - today).days
        if days_left < 0:
            return self.ExpiryStatus.EXPIRED
        elif days_left <= 7:
            return self.ExpiryStatus.EXPIRING_SOON
        return self.ExpiryStatus.SAFE

    @property
    def days_until_expiry(self) -> int:
        return (self.expiry_date - date.today()).days
