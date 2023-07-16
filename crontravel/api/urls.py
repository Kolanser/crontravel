from django.urls import include, path
from rest_framework import routers
from .views import (
#     CityViewSet,
    ExcursionListAPIView,
    ExcursionRetrieveAPIView,
    LocationListAPIView,
    LocationListExcursionsAPIView
#     CompanyViewSet,
#     ReviewViewSet
)

router = routers.DefaultRouter()
# router.register('locations', CityViewSet, basename='location')
# router.register('excursions', ExcursionViewSet, basename='excursion')
# router.register('companies', CompanyViewSet, basename='company')
# router.register(
#     r'excursions/(?P<excursion_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='review'
# )
urlpatterns = [
    path('', include(router.urls)),
    path('excursions/', ExcursionListAPIView.as_view(), name='excursion_list'),
    path('excursions/<int:excursion_id>/', ExcursionRetrieveAPIView.as_view(), name='excursions_detail'),
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path('locations/<int:location_id>/', LocationListExcursionsAPIView.as_view(), name='location-detail')
]
