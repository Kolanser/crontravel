from django.urls import include, path
from rest_framework import routers
from .views import (
    ExcursionListAPIView,
    ExcursionRetrieveAPIView,
    LocationListAPIView,
    LocationListExcursionsAPIView
)

router = routers.DefaultRouter()
urlpatterns = [
    path('', include(router.urls)),
    path(
        'excursions/',
        ExcursionListAPIView.as_view(),
        name='excursion_list'
    ),
    path(
        'excursions/<int:excursion_id>/',
        ExcursionRetrieveAPIView.as_view(),
        name='excursions_detail'
    ),
    path('locations/', LocationListAPIView.as_view(), name='location-list'),
    path(
        'locations/<int:location_id>/',
        LocationListExcursionsAPIView.as_view(),
        name='location-detail'
    ),
]
