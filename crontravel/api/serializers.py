from rest_framework import serializers
from excursions.models import (
    City,
    Excursion,
    ExcursionImage,
    Company,
    ExcursionProgram,
    ExcursionNotIncludePrice,
    ExcursionIncludePrice
)


class CompanySerializer(serializers.ModelSerializer):
    """Сериализатор тур компаний."""
    class Meta:
        model = Company
        fields = ('id', 'name', 'image', )

class CitySerializer(serializers.ModelSerializer):
    """Сериализатор городов (локаций)."""
    class Meta:
        model = City
        fields = ('id', 'name', 'description', )

class ExcursionImageSerializer(serializers.ModelSerializer):
    """Сериализатор фото экскурсий."""
    class Meta:
        model = ExcursionImage
        fields = ('image', )


class ExcursionProgramSerializer(serializers.ModelSerializer):
    """Сериализатор программ экскурсий."""
    class Meta:
        model = ExcursionProgram
        fields = ('title', 'locations', 'description')


class ExcursionNotIncludePriceSerializer(serializers.ModelSerializer):
    """Сериализатор программ экскурсий."""
    class Meta:
        model = ExcursionNotIncludePrice
        fields = ('service', )


class ExcursionIncludePriceSerializer(serializers.ModelSerializer):
    """Сериализатор что включено в стоимость экскурсий."""
    class Meta:
        model = ExcursionIncludePrice
        fields = ('service', )


class ExcursionListSerializer(serializers.ModelSerializer):
    """Сериализатор что не включено в стоимость экскурсий."""
    images = ExcursionImageSerializer(many=True, read_only=True)
    transport = serializers.CharField(
        source='get_transport_display'
    )

    class Meta:
        model = Excursion
        fields = (
            'id',
            'name',
            'duration',
            'size_group',
            'transport',
            'price',
            'images'
            # 'rating',
            # 'count_reviews'
        )


class ExcursionRetrieveSerializer(ExcursionListSerializer):
    """Сериализатор экскурсий."""
    company = CompanySerializer(read_only=True)
    type_excursion = serializers.CharField(
        source='get_type_excursion_display'
    )
    programs = ExcursionProgramSerializer(many=True, read_only=True)
    included_in_price = ExcursionIncludePriceSerializer(
        many=True,
        read_only=True
    )
    not_included_in_price = ExcursionNotIncludePriceSerializer(
        many=True,
        read_only=True
    )
    class Meta:
        model = Excursion
        fields = (
            'name',
            'images',
            'price',
            'children_age',
            'price_children',
            'description',
            'programs',
            'included_in_price',
            'not_included_in_price',
            'gathering_place',
            'starting_point',
            'company',
            'type_excursion',
            # 'reviews'
        )
