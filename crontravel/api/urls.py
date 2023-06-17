from django.urls import include, path
from rest_framework import routers
from .views import (
    CityViewSet,
    ExcursionViewSet,
    CompanyViewSet,
    ReviewViewSet
)

router = routers.DefaultRouter()
router.register('locations', CityViewSet, basename='location')
router.register('excursions', ExcursionViewSet, basename='excursion')
router.register('companies', CompanyViewSet, basename='company')
router.register(
    r'excursions/(?P<excursion_id>\d+)/reviews',
    ReviewViewSet,
    basename='review'
)
urlpatterns = [
    path('', include(router.urls)),
]