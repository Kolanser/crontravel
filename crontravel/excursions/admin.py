from django.contrib import admin
from .models import (
    Company,
    Excursion,
    City,
    ExcursionProgram,
    ExcursionNotIncludePrice,
    ExcursionIncludePrice,
    ExcursionImage,
    Category,
    Review,
    Application
)
from django.db.models import Avg


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}


class ExcursionProgramInline(admin.TabularInline):
    model = ExcursionProgram


class ExcursionNotIncludePriceInline(admin.TabularInline):
    model = ExcursionNotIncludePrice


class ExcursionIncludePriceInline(admin.TabularInline):
    model = ExcursionIncludePrice


class ExcursionImageInline(admin.TabularInline):
    model = ExcursionImage


@admin.register(Excursion)
class ExcursionAdmin(admin.ModelAdmin):
    """Админка экскурсий."""
    def show_description(self, object):
        """
        Отображение ограниченного количества
        символов описания в админке.
        """
        len_description = 32
        return object.description[:len_description] + '...'
    show_description.short_description = 'Описание'

    def rating(self, object):
        """
        Отображение рейтинга.
        """
        return object.reviews.filter(
            public=True
        ).aggregate(Avg('score'))['score__avg']
    rating.short_description = 'Рейтинг'

    def count_reviews(self, object):
        """
        Отображение рейтинга.
        """
        return object.reviews.filter(public=True).count()
    count_reviews.short_description = 'Количество оценок'

    list_display = (
        'id',
        'name',
        'price',
        'children_age',
        'price_children',
        'show_description',
        'author',
        'gathering_place',
        'company',
        'type_excursion',
        'transport',
        'size_group',
        'starting_point',
        'city',
        'rating',
        'count_reviews'
    )
    prepopulated_fields = {'slug': ('name',)}
    inlines = (
        ExcursionProgramInline,
        ExcursionNotIncludePriceInline,
        ExcursionIncludePriceInline,
        ExcursionImageInline
    )
    list_filter = (
        'price',
        'categories',
        'city',
        'type_excursion',
        'transport',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'excursion',
        'name',
        'ip',
        'pub_date',
        'text',
        'score',
        'public'
    )
    list_filter = (
        'excursion',
        'score',
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'excursion',
        'phone_number',
        'number_people',
        'number_children',
        'date',
        'comment',
    )
    list_filter = (
        'excursion',
    )
