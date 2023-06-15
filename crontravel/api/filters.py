from django_filters import FilterSet, ChoiceFilter, BooleanFilter
from excursions.models import Excursion, TYPE_CHOICES, TRANSPORT_CHOICES


class ExcursionFilter(FilterSet):
    """Фильтр для экскурсий."""
    type_excursion = ChoiceFilter(choices=TYPE_CHOICES)
    transport = ChoiceFilter(choices=TRANSPORT_CHOICES)


    class Meta:
        model = Excursion
        fields = ('city', 'categories', 'type_excursion', 'transport', )
