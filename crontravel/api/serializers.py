from rest_framework import serializers


class ExcursionMetaSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='meta_id')

class PhotoExcursionSerializer(serializers.Serializer):
    """Сериализатор фотографий экскурсии."""
    photo = serializers.CharField(
        label='Фото экскурсии',
        source='guid'
    )

class AgencyExcursionSerializer(serializers.Serializer):
    """Сериализатор агенства экскурсии."""
    name = serializers.CharField(
        label='Наименование туристического оператора',
    )
    image = serializers.CharField(
        label='Фото экскурсии',
        source='guid'
    )


class ExcursionRetrieveSerializer(serializers.Serializer):
    """Сериализатор для отправки обратной связи."""

# - Тур компания - Название, фото(лого)
# - Тип экскурсии - если групповая, то еще поле “Размер группы”
# - Отзывы - список отзывов со следующими полями
#     - Имя
#     - Дата
#     - Оценка
#     - Описание
    id = serializers.IntegerField(
        source='ID',
        read_only=True,
    )
    title = serializers.CharField(
        label='Наименование экскурсии',
        source='post_title'
    )
    duration = serializers.CharField(
        label='Длительность экскурсии',
        source='excursion-duration',
        required=False
    )
    description = serializers.CharField(
        label='Описание экскурсии',
        source='post_content',
        required=False
    )
    movement = serializers.CharField(
        label='Транспорт',
        source='excursion-movement',
        required=False
    )
    price = serializers.CharField(
        label='Цена за человека',
        source='tour-price',
        required=False
    )
    price_children = serializers.CharField(
        label='Цена за ребенка',
        source='tour-price_children',
        required=False
    )
    children_age = serializers.CharField(
        label='Возраст ребенка',
        source='tour-price_children-age',
        required=False
    )
    start_coordinates = serializers.CharField(
        label='Место сбора (координаты)',
        source='excursion-map_yandex',
        required=False
    )
    photos = PhotoExcursionSerializer(
        many=True,
        read_only=True,
        label='Фото',
        required=False 
    )
    rating = serializers.FloatField(
        label='Оценка(рейтинг)',
        required=False 
    )
    comment_count = serializers.IntegerField(
        label='Количество комментариев',
        read_only=True,
    )
    band_size = serializers.CharField(
        label='Количество человек в экскурсии',
        source='excursion-band-size',
        required=False 
    )
    start_city = serializers.CharField(
        label = 'Точка старта',
        source='excursion-start-city',
        required=False 
    )
    agency = AgencyExcursionSerializer(read_only=True)

class LocationListSerializer(serializers.Serializer):
    """Сериализатор для списка городов."""
    id = serializers.IntegerField(source='term_id')
    name = serializers.CharField()


class LocationListExcursionsSerializer(serializers.Serializer):
    """Сериализатор для списка городов."""
    id = serializers.IntegerField(source='ID')
    title = serializers.CharField(
        label='Наименование экскурсии',
        source='post_title'
    )
    duration = serializers.CharField(
        label='Длительность экскурсии',
        source='excursion-duration',
        required=False
    )
    movement = serializers.CharField(
        label='Транспорт',
        source='excursion-movement',
        required=False
    )
    price = serializers.CharField(
        label='Цена за человека',
        source='tour-price',
        required=False
    )
    photo = serializers.CharField(
        label='Фото',
        required=False 
    )
    raiting = serializers.FloatField(
        label='Оценка(рейтинг)',
        required=False 
    )
    comment_count = serializers.IntegerField(
        label='Количество комментариев',
        help_text = 'dddd',
        read_only=True,
    )
    band_size = serializers.CharField(
        label='Количество человек в экскурсии',
        source='excursion-band-size',
        required=False 
    )
    excursion_format = serializers.CharField(
        label='Формат экскурсии',
        required=False 
    )




# from excursions.models import (
#     City,
#     Excursion,
#     ExcursionImage,
#     Company,
#     ExcursionProgram,
#     ExcursionNotIncludePrice,
#     ExcursionIncludePrice,
#     Review,
#     Application
# )


# class CompanySerializer(serializers.ModelSerializer):
#     """Сериализатор тур компаний."""
#     class Meta:
#         model = Company
#         fields = ('id', 'name', 'image', )


# class CitySerializer(serializers.ModelSerializer):
#     """Сериализатор городов (локаций)."""
#     class Meta:
#         model = City
#         fields = ('id', 'name', 'description', )


# class ExcursionImageSerializer(serializers.ModelSerializer):
#     """Сериализатор фото экскурсий."""
#     class Meta:
#         model = ExcursionImage
#         fields = ('image', )


# class ExcursionProgramSerializer(serializers.ModelSerializer):
#     """Сериализатор программ экскурсий."""
#     class Meta:
#         model = ExcursionProgram
#         fields = ('title', 'locations', 'description')


# class ExcursionNotIncludePriceSerializer(serializers.ModelSerializer):
#     """Сериализатор программ экскурсий."""
#     class Meta:
#         model = ExcursionNotIncludePrice
#         fields = ('service', )


# class ExcursionIncludePriceSerializer(serializers.ModelSerializer):
#     """Сериализатор что включено в стоимость экскурсий."""
#     class Meta:
#         model = ExcursionIncludePrice
#         fields = ('service', )


# class ReviewSerializer(serializers.ModelSerializer):
#     """Сериализатор получение отзывов."""
#     class Meta:
#         model = Review
#         fields = (
#             'name',
#             'pub_date',
#             'text',
#             'score'
#         )


# class ReviewWriteSerializer(serializers.ModelSerializer):
#     """Сериализатор добавления отзывов."""
#     class Meta:
#         model = Review
#         fields = (
#             'name',
#             'text',
#             'score'
#         )


# class ExcursionListSerializer(serializers.ModelSerializer):
#     """Сериализатор что не включено в стоимость экскурсий."""
#     image = serializers.SerializerMethodField(read_only=True)
#     transport = serializers.CharField(
#         source='get_transport_display'
#     )
#     rating = serializers.FloatField()
#     count_reviews = serializers.IntegerField()

#     class Meta:
#         model = Excursion
#         fields = (
#             'id',
#             'name',
#             'duration',
#             'size_group',
#             'transport',
#             'price',
#             'image',
#             'rating',
#             'count_reviews'
#         )

#     def get_image(self, obj):
#         if obj.images.exists():
#             request = self.context.get('request')
#             image_url = obj.images.first().image.url
#             return request.build_absolute_uri(image_url)


# class ExcursionRetrieveSerializer(ExcursionListSerializer):
#     """Сериализатор экскурсий."""
#     images = ExcursionImageSerializer(many=True, read_only=True)
#     company = CompanySerializer(read_only=True)
#     type_excursion = serializers.CharField(
#         source='get_type_excursion_display'
#     )
#     programs = ExcursionProgramSerializer(many=True, read_only=True)
#     included_in_price = ExcursionIncludePriceSerializer(
#         many=True,
#         read_only=True
#     )
#     not_included_in_price = ExcursionNotIncludePriceSerializer(
#         many=True,
#         read_only=True
#     )

#     class Meta:
#         model = Excursion
#         fields = (
#             'name',
#             'images',
#             'price',
#             'children_age',
#             'price_children',
#             'description',
#             'programs',
#             'included_in_price',
#             'not_included_in_price',
#             'gathering_place',
#             'starting_point',
#             'company',
#             'type_excursion',
#         )


# class ApplicationSerializer(serializers.ModelSerializer):
#     """Сериализатор добавления отзывов."""

#     class Meta:
#         model = Application
#         fields = (
#             'name',
#             'phone_number',
#             'number_people',
#             'number_children',
#             'date',
#             'comment',
#         )
