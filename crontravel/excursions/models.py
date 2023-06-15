from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator

PERSON = 'PRS'
GROUP = 'GRP'
TYPE_CHOICES = [
    (PERSON, 'Частная'),
    (GROUP, 'Групповая'),
]
AVTO = 'AVT'
WALK = 'WLK'
TRANSPORT_CHOICES = [
    (AVTO, 'Автомобиль'),
    (WALK, 'Пешая'),
]

MAX_AGE_CHILDREN = 17


class Company(models.Model):
    """Модель туристической компании."""
    name = models.CharField(
        verbose_name='Название туристической компании',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Фото (логотип) компании',
        upload_to='excursions/',
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Туристическая компания'
        verbose_name_plural = 'Туристические компании'

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(
        verbose_name='Название категории',
        max_length=64
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


class Excursion(models.Model):
    """Модель экскурсии."""
    name = models.CharField(
        verbose_name='Название экскурсии',
        max_length=64
    )
    price = models.PositiveIntegerField(verbose_name='Стоимость')
    children_age = models.PositiveIntegerField(
        verbose_name='Ограничение возраста детей',
        help_text='Количество лет',
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(
                MAX_AGE_CHILDREN,
                f'Максимальный возраст ребенка {MAX_AGE_CHILDREN}.'
            )
        ]
    )
    price_children = models.PositiveIntegerField(
        verbose_name='Стоимость для ребенка'
    )
    description = models.TextField(verbose_name='Описание')
    author = models.ForeignKey(
        get_user_model(),
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший экскурсию',
        on_delete=models.SET_NULL,
        null=True
    )
    slug = models.SlugField(unique=True)
    gathering_place = models.CharField(
        'Место сбора',
        help_text='Адрес и координаты(для отображения точки на карте)',
        max_length=32,
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        verbose_name='Туристическая компания',
        related_name='companies'
    )
    type_excursion = models.CharField(
        'Тип экскурсии',
        max_length=3,
        choices=TYPE_CHOICES,
        default=GROUP,
    )
    transport = models.CharField(
        'Транспорт',
        max_length=3,
        choices=TRANSPORT_CHOICES,
        default=AVTO,
    )
    size_group = models.CharField(
        'Размер группы',
        max_length=32,
    )
    starting_point = models.CharField(
        'Точка старта',
        max_length=64,
    )
    city = models.ForeignKey(
        'City',
        verbose_name='Город (локация, направление)',
        related_name='excursions',
        on_delete=models.CASCADE
    )
    categories = models.ManyToManyField(
        'Category',
        verbose_name='Категории',
        related_name='excursions',
    )

    class Meta:
        verbose_name = 'Экскурсия'
        verbose_name_plural = 'Экскурсии'

    def __str__(self) -> str:
        return f'{self.name} - {self.company}'


class City(models.Model):
    """Модель города."""
    name = models.CharField(
        'Город',
        max_length=32,
        unique=True
    )
    description = models.TextField(verbose_name='Описание города')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

    def __str__(self) -> str:
        return self.name


class ExcursionProgram(models.Model):
    """Модель программы экскурсии."""
    excursion = models.ForeignKey(
        'Excursion',
        on_delete=models.CASCADE,
        related_name='programs',
        verbose_name='Экскурсия',
    )
    title = models.CharField(
        'Название (номер) дня',
        max_length=32,
    )
    locations = models.CharField(
        'Локации',
        max_length=128,
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Программа по дням экскурсии'
        verbose_name_plural = 'Программы по дням экскурсии'


class ExcursionNotIncludePrice(models.Model):
    """Модель, что не включено в стоимость экскурсии."""
    excursion = models.ForeignKey(
        'Excursion',
        on_delete=models.CASCADE,
        related_name='not_included_in_price',
        verbose_name='Экскурсия',
    )
    service = models.CharField(
        verbose_name='Услуга',
        help_text='Оплачивается отдельно',
        max_length=128
    )

    class Meta:
        verbose_name = 'Не включено в стоимость экскурсии'
        verbose_name_plural = 'Не включено в стоимость экскурсии'


class ExcursionIncludePrice(models.Model):
    """Модель, что включено в стоимость экскурсии."""
    excursion = models.ForeignKey(
        'Excursion',
        on_delete=models.CASCADE,
        related_name='included_in_price',
        verbose_name='Экскурсия',
    )
    service = models.CharField(
        verbose_name='Услуга',
        help_text='Включено в стоимость экскурсии',
        max_length=128
    )

    class Meta:
        verbose_name = 'Включено в стоимость экскурсии'
        verbose_name_plural = 'Включено в стоимость экскурсии'


class ExcursionImage(models.Model):
    """Модель фотографий экскурсии."""
    excursion = models.ForeignKey(
        'Excursion',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Экскурсия',
    )
    image = models.ImageField(
        verbose_name='Фото экскурсии',
        upload_to='excursions/',
    )

    class Meta:
        verbose_name = 'Фото экскурсий'
        verbose_name_plural = 'Фото экскурсий'


# - Отзывы - список отзывов со следующими полями
#     - Имя
#     - Дата
#     - Оценка
#     - Описание
