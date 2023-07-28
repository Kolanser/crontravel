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


class CommentExcursionSerializer(serializers.Serializer):
    """Сериализатор комментариев экскурсии."""
    author = serializers.CharField(
        label='Автор комментария',
        source='comment_author'
    )
    date = serializers.CharField(
        label='Дата комментария',
        source='comment_date'
    )
    comment = serializers.CharField(
        label='Комментарий',
        source='comment_content'
    )


class ExcursionRetrieveSerializer(serializers.Serializer):
    """Сериализатор для отправки обратной связи."""

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
    type_excursion = serializers.CharField(
        label='Тип экскурсии',
        source='type',
        required=False
    )
    band_size = serializers.CharField(
        label='Количество человек в экскурсии',
        source='excursion-band-size',
        required=False
    )
    start_city = serializers.CharField(
        label='Точка старта',
        source='excursion-start-city',
        required=False
    )
    agency = AgencyExcursionSerializer(read_only=True)
    comments = CommentExcursionSerializer(
        read_only=True,
        required=False,
        many=True
    )


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
