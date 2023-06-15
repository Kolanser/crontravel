from django.urls import include, path
from rest_framework import routers
from .views import (
    CityViewSet,
    ExcursionViewSet,
    CompanyViewSet,
)

router = routers.DefaultRouter()
router.register('locations', CityViewSet, basename='location')
router.register('excursions', ExcursionViewSet, basename='excursion')
router.register('companies', ExcursionViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
]