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
    ExcursionRetrieveSerializer,
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
    serializer_class = ExcursionRetrieveSerializer
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
    serializer_class = ExcursionRetrieveSerializer

    def get_object(self):
        with connection.cursor() as cursor:
            excursion_id = self.kwargs['excursion_id']
            cursor.execute(
                """
                SELECT * FROM wp_posts 
                WHERE post_type = "excursions" and post_status = "publish"
                AND ID = %s
                """,
                [excursion_id]
            )
            obj = dictfetchall(cursor)
        if not obj:
            raise Http404
        with connection.cursor() as cursor:
            excursion_id = self.kwargs['excursion_id']
            cursor.execute(
                """
                SELECT * FROM wp_postmeta
                where post_id = %s
                """,
                [excursion_id]
            )
            excursion_meta = dictfetchall(cursor)
        excursion_meta_dict = {meta['meta_key']:meta['meta_value'] for meta in excursion_meta}
        excursion = obj[0] | excursion_meta_dict
        count_photo = excursion.get('excursion-gallery')
        if count_photo:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT wp_posts.guid
                    FROM wp_postmeta
                    INNER JOIN wp_posts
                    ON wp_posts.ID = wp_postmeta.meta_value
                    WHERE wp_postmeta.post_id = %s
                    AND meta_key
                    LIKE "excursion-gallery_%%_excursion-gallery-image"
                    """,
                    [excursion_id]
                )
                excursion['photos'] = dictfetchall(cursor)
        return excursion    


class LocationListAPIView(generics.ListAPIView):
    """Получение списка городов."""
    serializer_class = LocationListSerializer

    def get_queryset(self):
        results = []
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT term_id, name
                FROM wp_terms
                WHERE term_id IN (
                    SELECT DISTINCT term_id
                    FROM wp_term_taxonomy
                    WHERE taxonomy = "location")
                """
            )
            results = dictfetchall(cursor)
        return results


class LocationListExcursionsAPIView(generics.ListAPIView):
    """Получение списка экскурсий по городу."""
    serializer_class = LocationListExcursionsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        results = []
        with connection.cursor() as cursor:
            location_id = self.kwargs['location_id']
            cursor.execute(
                """
                SELECT posts.*, wp_terms.name as excursion_format
                FROM wp_posts posts
                INNER JOIN wp_term_relationships relationships
                ON posts.ID = relationships.object_id
                INNER JOIN wp_terms
                ON wp_terms.term_id = relationships.term_taxonomy_id
                WHERE post_type = "excursions"
                AND post_status = "publish"
                AND ID in (
                    SELECT object_id 
                    FROM wp_term_relationships
                    WHERE term_taxonomy_id = (
                        SELECT term_taxonomy_id
                        FROM wp_term_taxonomy
                        WHERE taxonomy = "location"
                            AND term_id = %s
                        )
                    )
                AND relationships.term_taxonomy_id in 
                    (
                        SELECT term_taxonomy_id FROM wp_term_taxonomy
                        WHERE term_id in 
                            (
                            SELECT term_id FROM wp_terms
                            WHERE slug in ("group", "individual")
                            )
                    )
                ORDER BY posts.menu_order
                """,
                [location_id]
            )
            results = dictfetchall(cursor)
        group_slug = 'group'
        individual_slug = 'individual'
        ids_excursion = []
        for excursion in results:
            ids_excursion.append(excursion['ID'])
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM b0crontrav_betact.wp_postmeta
                where post_id in %s
                """,
                [ids_excursion]
            )
            excursion_meta = dictfetchall(cursor)
        for index, excursion in enumerate(results):
            for meta in excursion_meta:
                if meta['post_id'] == excursion['ID']:
                    meta_key = meta['meta_key']
                    results[index][meta_key] = meta['meta_value']
                    excursion_meta.remove(meta)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT meta.post_id, posts.guid
                FROM wp_postmeta as meta
                JOIN wp_posts as posts
                ON meta.meta_value = posts.ID
                WHERE meta.post_id in %s
                AND meta.meta_key = "_thumbnail_id"
                """,
                [ids_excursion]
            )
            excursion_photos = dictfetchall(cursor)
        for index, excursion in enumerate(results):
            for excursion_photo in excursion_photos:
                if excursion_photo['post_id'] == excursion['ID']:
                    results[index]['photo'] = excursion_photo['guid']
                    excursion_photos.remove(excursion_photo)
        if not results:
            raise Http404
        return results
