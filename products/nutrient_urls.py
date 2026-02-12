from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NutrientTypeViewSet

router = DefaultRouter()
router.register('', NutrientTypeViewSet, basename='nutrient')

urlpatterns = [
    path('', include(router.urls)),
]