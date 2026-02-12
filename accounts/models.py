from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    assigned_store = models.ForeignKey(
        'stores.Store',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='staff_members'
    )

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def is_staff_role(self):
        return self.roles.filter(role__in=['admin', 'staff']).exists()

    @property
    def is_customer_role(self):
        return self.roles.filter(role='customer').exists()


class Role(models.Model):
    class RoleType(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        STAFF = 'staff', 'Staff'
        CUSTOMER = 'customer', 'Customer'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    role = models.CharField(
        max_length=20,
        choices=RoleType.choices
    )
    store = models.ForeignKey(
        'stores.Store',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Store scope for staff roles"
    )

    class Meta:
        unique_together = ['user', 'role', 'store']

    def __str__(self):
        store_name = self.store.name if self.store else 'Global'
        return f"{self.user.username} - {self.role} @ {store_name}"