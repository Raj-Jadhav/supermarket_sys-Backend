from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from accounts.permissions import IsStaffUser
from .models import Category, NutrientType, Product
from .serializers import (
    CategorySerializer, NutrientTypeSerializer,
    ProductSerializer, ProductDetailSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]


class NutrientTypeViewSet(viewsets.ModelViewSet):
    queryset = NutrientType.objects.all()
    serializer_class = NutrientTypeSerializer
    filterset_fields = ['category']
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related(
        'categories', 'nutrients'
    )
    filterset_fields = ['categories', 'nutrients__category', 'is_active']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'price', 'created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]
