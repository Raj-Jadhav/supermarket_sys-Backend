from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from accounts.permissions import IsStaffUser
from .models import StockItem
from .serializers import AddStockSerializer, StockItemSerializer, UpdateStockSerializer
from .services import StockService, ExpiryService


class StockListView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        """List all stock items in a store."""
        stock = StockItem.objects.filter(
            aisle__store_id=store_id
        ).select_related('product', 'aisle', 'aisle__store')
        serializer = StockItemSerializer(stock, many=True)
        return Response(serializer.data)

    def post(self, request, store_id):
        """Add stock with aisle-category validation."""
        serializer = AddStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            stock = StockService.add_stock(
                product_id=serializer.validated_data['product_id'],
                aisle_id=serializer.validated_data['aisle_id'],
                quantity=serializer.validated_data['quantity'],
                expiry_date=serializer.validated_data.get('expiry_date'),
                batch_number=serializer.validated_data.get('batch_number', ''),
            )
            return Response(
                StockItemSerializer(stock).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response(
                {'error': e.message_dict if hasattr(e, 'message_dict') else str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class StockDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def put(self, request, store_id, pk):
        serializer = UpdateStockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            stock = StockService.update_stock_quantity(
                pk, serializer.validated_data['quantity']
            )
            return Response(StockItemSerializer(stock).data)
        except StockItem.DoesNotExist:
            return Response(
                {'error': 'Stock item not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, store_id, pk):
        try:
            stock = StockItem.objects.get(id=pk, aisle__store_id=store_id)
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except StockItem.DoesNotExist:
            return Response(
                {'error': 'Stock item not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class ExpiringStockView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        items = ExpiryService.get_expiring_stock(store_id)
        return Response(StockItemSerializer(items, many=True).data)


class ExpiredStockView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        items = ExpiryService.get_expired_stock(store_id)
        return Response(StockItemSerializer(items, many=True).data)


class LowStockView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        items = ExpiryService.get_low_stock(store_id)
        return Response(StockItemSerializer(items, many=True).data)


class StockAlertsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffUser]

    def get(self, request, store_id):
        alerts = ExpiryService.get_stock_alerts(store_id)
        return Response(alerts)
