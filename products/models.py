from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True,
                           help_text="Icon name (e.g. apple, beef, milk)")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class NutrientType(models.Model):
    class NutrientCategory(models.TextChoices):
        PROTEIN = 'protein', 'Protein'
        CARBOHYDRATE = 'carb', 'Carbohydrate'
        VITAMIN = 'vitamin', 'Vitamin'
        FAT = 'fat', 'Fat'
        MINERAL = 'mineral', 'Mineral'
        FIBER = 'fiber', 'Fiber'

    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20,
        choices=NutrientCategory.choices
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']
        unique_together = ['name', 'category']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(
        Category,
        related_name='products'
    )
    nutrients = models.ManyToManyField(
        NutrientType,
        related_name='products',
        blank=True
    )
    shelf_life_days = models.PositiveIntegerField(
        default=30,
        help_text="Number of days before expiry from stock date"
    )
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_nutrient_summary(self):
        return list(self.nutrients.values_list('name', flat=True))

    def get_category_names(self):
        return list(self.categories.values_list('name', flat=True))
