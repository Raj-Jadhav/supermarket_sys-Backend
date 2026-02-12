from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from .services import ProductSearchService


class ProductSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, store_id):
        query = request.query_params.get('q', '').strip()
        search_type = request.query_params.get('type', 'all')

        if not query:
            return Response(
                {'error': 'Search query "q" is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if search_type not in ('all', 'product', 'nutrient', 'category'):
            return Response(
                {'error': 'Invalid search type. Use: all, product, nutrient, category.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = ProductSearchService.search_products(
            store_id=store_id,
            query=query,
            search_type=search_type,
            user=request.user if request.user.is_authenticated else None
        )

        return Response({
            'query': query,
            'search_type': search_type,
            'results_count': len(results),
            'results': results,
        })