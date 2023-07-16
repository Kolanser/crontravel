from rest_framework import mixins, viewsets, status, generics
# from excursions.models import City, Excursion, Company
# from api.serializers import (
#     CitySerializer,
#     ExcursionRetrieveSerializer,
#     ExcursionListSerializer,
#     CompanySerializer,
#     ReviewSerializer,
#     ReviewWriteSerializer,
#     ApplicationSerializer,
# )
from django_filters.rest_framework import DjangoFilterBackend
# from .filters import ExcursionFilter
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from rest_framework.views import APIView
from .serializers import (
    ExcursionSerializer,
    LocationListSerializer,
    LocationListExcursionsSerializer,
)
from django.http import Http404
from django.db import connection


# class ExcursionViewSet(viewsets.ReadOnlyModelViewSet):
#     """Получение экскурсий."""
#     queryset = Excursion.objects.all()
#     queryset = Excursion.objects.annotate(
#         rating=Avg('reviews__score'),
#         count_reviews=Count('reviews')
#     )
#     serializer_class = ExcursionRetrieveSerializer
#     filter_backends = (DjangoFilterBackend, )
#     filterset_class = ExcursionFilter
#     pagination_class = PageNumberPagination
#     filter_backends = (SearchFilter, )
#     search_fields = ('city__name', 'gathering_place', 'starting_point', )

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return ExcursionListSerializer
#         return ExcursionRetrieveSerializer

#     @action(methods=['post'], detail=True)
#     def application(self, request, pk):
#         """Подать заявку на экскурсию."""
#         serializer = ApplicationSerializer(data=request.data)
#         if serializer.is_valid():
#             excursion = self.get_object()
#             serializer.save(excursion=excursion)
#             return Response(
#                 {'status': 'Заявка успешно отправлена'},
#                 status=status.HTTP_200_OK
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )


# class CompanyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
#     """Получение тур компаний."""
#     queryset = Company.objects.all()
#     serializer_class = CompanySerializer


# class ReviewViewSet(viewsets.ModelViewSet):
#     """Получение и добавление отзывов."""

#     def get_serializer_class(self):
#         if self.request.method in ('POST', 'PATCH', 'PUT',):
#             return ReviewWriteSerializer
#         return ReviewSerializer

#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip

#     def get_queryset(self, *args, **kwargs):
#         excursion_id = int(self.kwargs.get('excursion_id'))
#         excursion = get_object_or_404(Excursion, id=excursion_id)
#         return excursion.reviews.filter(public=True)

#     def perform_create(self, serializer):
#         excursion_id = self.kwargs.get('excursion_id')
#         excursion = get_object_or_404(Excursion, id=excursion_id)
#         ip = self.get_client_ip(self.request)
#         serializer.save(
#             excursion=excursion,
#             ip=ip,
#             public=False
#         )


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class ExcursionListAPIView(generics.ListAPIView):
    """Получение списка экскурсий."""
    serializer_class = ExcursionSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM b0crontrav_betact.wp_posts 
                WHERE post_type = "excursions" and post_status = "publish"
                """
            )
            results = dictfetchall(cursor)
        return results


class ExcursionRetrieveAPIView(generics.RetrieveAPIView):
    """Получение отдельной экскурсию."""
    serializer_class = ExcursionSerializer

    def get_object(self):
        with connection.cursor() as cursor:
            excursion_id = self.kwargs['excursion_id']
            cursor.execute(
                """
                SELECT * FROM b0crontrav_betact.wp_posts 
                WHERE post_type = "excursions" and post_status = "publish"
                AND ID = %s
                """,
                [excursion_id]
            )
            obj = dictfetchall(cursor)
        try:
            return obj[0]
        except:
            raise Http404


class LocationListAPIView(generics.ListAPIView):
    """Получение списка городов."""
    serializer_class = LocationListSerializer

    def get_queryset(self):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT term_id, name
                FROM b0crontrav_betact.wp_terms
                WHERE term_id IN (
                    SELECT DISTINCT term_id
                    FROM b0crontrav_betact.wp_term_taxonomy
                    WHERE taxonomy = "location")
                """
            )
            results = dictfetchall(cursor)
        return results

class LocationListExcursionsAPIView(generics.ListAPIView):
    """Получение списка экскурсий по городу."""
    serializer_class = LocationListExcursionsSerializer

    def get_queryset(self):
        results = []
        with connection.cursor() as cursor:
            location_id = self.kwargs['location_id']
            cursor.execute(
                """
                SELECT * FROM b0crontrav_betact.wp_posts
                where post_type = "excursions"
                and post_status = "publish"
                and ID in (SELECT object_id FROM b0crontrav_betact.wp_term_relationships
                WHERE term_taxonomy_id = 
                    (SELECT term_taxonomy_id FROM b0crontrav_betact.wp_term_taxonomy
                    WHERE taxonomy = "location"
                    AND term_id = %s)
                )
                """,
                [location_id]
            )
            results = dictfetchall(cursor)
        if not results:
            raise Http404
        return results

# class ExcursionViewSet(viewsets.GenericViewSet):
#     serializer_class = ExcursionSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         results = []
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT * FROM b0crontrav_betact.wp_posts 
#                 WHERE post_type = "excursions" and post_status = "publish"
#                 """
#             )
#             results = dictfetchall(cursor)
#         return results

#     def get_object(self):
#         with connection.cursor() as cursor:
#             excursion_id = self.kwargs['pk']
#             cursor.execute(
#                 """
#                 SELECT * FROM b0crontrav_betact.wp_posts 
#                 WHERE post_type = "excursions" and post_status = "publish"
#                 and ID = %s
#                 """,
#                 [excursion_id]
#             )
#             obj = dictfetchall(cursor)
#         try:
#             return obj[0]
#         except:
#             raise Http404

#     def list(self, request):
#         queryset = self.get_queryset()
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         excursion = self.get_object()
#         serializer = self.serializer_class(excursion)
#         return Response(serializer.data)
    