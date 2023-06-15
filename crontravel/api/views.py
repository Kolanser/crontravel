from rest_framework import filters, generics, status, viewsets
from excursions.models import City, Excursion, Company
from api.serializers import (
    CitySerializer,
    ExcursionRetrieveSerializer,
    ExcursionListSerializer,
    CompanySerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExcursionFilter


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение городов."""
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ExcursionViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение экскурсий."""
    queryset = Excursion.objects.all()
    serializer_class = ExcursionRetrieveSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ExcursionFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ExcursionListSerializer
        return ExcursionRetrieveSerializer


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение тур компаний."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer