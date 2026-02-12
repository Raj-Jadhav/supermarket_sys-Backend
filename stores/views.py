from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.permissions import IsStaffUser, IsAdminUser
from .models import Store, Aisle
from .serializers import StoreSerializer, AisleSerializer, AisleDetailSerializer


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.filter(is_active=True)
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]


class AisleViewSet(viewsets.ModelViewSet):
    serializer_class = AisleSerializer

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        return Aisle.objects.filter(store_id=store_id).prefetch_related(
            'allowed_categories', 'stock_items'
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AisleDetailSerializer
        return AisleSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated(), IsStaffUser()]

    def perform_create(self, serializer):
        store_id = self.kwargs.get('store_id')
        serializer.save(store_id=store_id)

    @action(detail=True, methods=['post'], url_path='categories')
    def add_category(self, request, store_id=None, pk=None):
        """Add allowed category to an aisle."""
        aisle = self.get_object()
        category_ids = request.data.get('category_ids', [])
        aisle.allowed_categories.add(*category_ids)
        return Response(AisleSerializer(aisle).data)

    @action(detail=True, methods=['delete'], url_path='categories/(?P<cat_id>[^/.]+)')
    def remove_category(self, request, store_id=None, pk=None, cat_id=None):
        """Remove allowed category from an aisle."""
        aisle = self.get_object()
        aisle.allowed_categories.remove(cat_id)
        return Response(AisleSerializer(aisle).data)
