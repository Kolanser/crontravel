from rest_framework import mixins, viewsets, status
from excursions.models import City, Excursion, Company
from api.serializers import (
    CitySerializer,
    ExcursionRetrieveSerializer,
    ExcursionListSerializer,
    CompanySerializer,
    ReviewSerializer,
    ReviewWriteSerializer,
    ApplicationSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ExcursionFilter
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Получение городов."""
    queryset = City.objects.all()
    serializer_class = CitySerializer


class ExcursionViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение экскурсий."""
    queryset = Excursion.objects.all()
    queryset = Excursion.objects.annotate(
        rating=Avg('reviews__score'),
        count_reviews=Count('reviews')
    )
    serializer_class = ExcursionRetrieveSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ExcursionFilter
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ExcursionListSerializer
        return ExcursionRetrieveSerializer

    @action(methods=['post'], detail=True)
    def application(self, request, pk):
        """Подать заявку на экскурсию."""
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            excursion = self.get_object()
            serializer.save(excursion=excursion)
            return Response(
                {'status': 'Заявка успешно отправлена'},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class CompanyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Получение тур компаний."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Получение и добавление отзывов."""

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT',):
            return ReviewWriteSerializer
        return ReviewSerializer

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_queryset(self, *args, **kwargs):
        excursion_id = int(self.kwargs.get('excursion_id'))
        excursion = get_object_or_404(Excursion, id=excursion_id)
        return excursion.reviews.filter(public=True)

    def perform_create(self, serializer):
        excursion_id = self.kwargs.get('excursion_id')
        excursion = get_object_or_404(Excursion, id=excursion_id)
        ip = self.get_client_ip(self.request)
        serializer.save(
            excursion=excursion,
            ip=ip,
            public=False
        )
