from django_filters import FilterSet, ChoiceFilter, NumberFilter
from excursions.models import Excursion, TYPE_CHOICES, TRANSPORT_CHOICES


class ExcursionFilter(FilterSet):
    """Фильтр для экскурсий."""
    type_excursion = ChoiceFilter(choices=TYPE_CHOICES)
    transport = ChoiceFilter(choices=TRANSPORT_CHOICES)
    min_rating = NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = NumberFilter(field_name='rating', lookup_expr='lte')
    min_price = NumberFilter(field_name='price', lookup_expr='gte')
    max_price = NumberFilter(field_name='price', lookup_expr='lte')


    class Meta:
        model = Excursion
        fields = (
            'city',
            'categories',
            'type_excursion',
            'transport',
            'min_rating',
            'max_rating',
            'min_price',
            'max_price',
            )
