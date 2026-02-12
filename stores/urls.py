from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, AisleViewSet

router = DefaultRouter()
router.register('', StoreViewSet, basename='store')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:store_id>/aisles/',
         AisleViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='aisle-list'),
    path('<int:store_id>/aisles/<int:pk>/',
         AisleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='aisle-detail'),
    path('<int:store_id>/aisles/<int:pk>/categories/',
         AisleViewSet.as_view({'post': 'add_category'}),
         name='aisle-add-category'),
    # Inventory & Search URLs nested under stores
    path('<int:store_id>/stock/', include('inventory.urls')),
    path('<int:store_id>/search/', include('search.urls')),
    path('<int:store_id>/analytics/', include('analytics.urls')),
]