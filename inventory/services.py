from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.db.models import Sum

from products.models import Product
from stores.models import Aisle
from .models import StockItem


class StockService:
    @staticmethod
    def add_stock(product_id: int, aisle_id: int, quantity: int,
                  expiry_date=None, batch_number='') -> StockItem:
        """
        Add stock with category validation.
        Raises ValidationError if product doesn't match aisle categories.
        """
        product = Product.objects.get(id=product_id)
        aisle = Aisle.objects.get(id=aisle_id)

        # Validate category match
        product_categories = set(product.categories.values_list('id', flat=True))
        allowed_categories = set(aisle.allowed_categories.values_list('id', flat=True))

        if allowed_categories and not (product_categories & allowed_categories):
            raise ValidationError({
                'aisle': (
                    f"Cannot place '{product.name}' in '{aisle.name}'. "
                    f"Product categories don't match aisle requirements."
                ),
                'product_categories': list(
                    product.categories.values_list('name', flat=True)
                ),
                'allowed_categories': list(
                    aisle.allowed_categories.values_list('name', flat=True)
                ),
            })

        calc_expiry = expiry_date or (
            date.today() + timedelta(days=product.shelf_life_days)
        )

        stock = StockItem.objects.create(
            product=product,
            aisle=aisle,
            quantity=quantity,
            expiry_date=calc_expiry,
            batch_number=batch_number,
        )
        return stock

    @staticmethod
    def update_stock_quantity(stock_id: int, quantity: int) -> StockItem:
        stock = StockItem.objects.get(id=stock_id)
        stock.quantity = quantity
        stock.save()
        return stock


class ExpiryService:
    @staticmethod
    def get_expiring_stock(store_id: int, days_threshold: int = 7):
        cutoff = date.today() + timedelta(days=days_threshold)
        return StockItem.objects.filter(
            aisle__store_id=store_id,
            expiry_date__lte=cutoff,
            expiry_date__gte=date.today(),
            quantity__gt=0
        ).select_related('product', 'aisle')

    @staticmethod
    def get_expired_stock(store_id: int):
        return StockItem.objects.filter(
            aisle__store_id=store_id,
            expiry_date__lt=date.today(),
            quantity__gt=0
        ).select_related('product', 'aisle')

    @staticmethod
    def get_low_stock(store_id: int, threshold: int = 10):
        return StockItem.objects.filter(
            aisle__store_id=store_id,
            quantity__lte=threshold,
            quantity__gt=0
        ).select_related('product', 'aisle')

    @staticmethod
    def get_stock_alerts(store_id: int):
        expiring = ExpiryService.get_expiring_stock(store_id)
        expired = ExpiryService.get_expired_stock(store_id)
        low = ExpiryService.get_low_stock(store_id)

        return {
            'expiring_soon': {
                'count': expiring.count(),
                'items': [
                    {
                        'id': item.id,
                        'product': item.product.name,
                        'aisle': f"Aisle {item.aisle.number} ({item.aisle.name})",
                        'quantity': item.quantity,
                        'days_left': item.days_until_expiry,
                        'expiry_date': str(item.expiry_date),
                    }
                    for item in expiring[:15]
                ],
            },
            'expired': {
                'count': expired.count(),
                'items': [
                    {
                        'id': item.id,
                        'product': item.product.name,
                        'aisle': f"Aisle {item.aisle.number} ({item.aisle.name})",
                        'quantity': item.quantity,
                        'expired_days': abs(item.days_until_expiry),
                    }
                    for item in expired[:15]
                ],
            },
            'low_stock': {
                'count': low.count(),
                'items': [
                    {
                        'id': item.id,
                        'product': item.product.name,
                        'aisle': f"Aisle {item.aisle.number} ({item.aisle.name})",
                        'quantity': item.quantity,
                    }
                    for item in low[:15]
                ],
            },
        }