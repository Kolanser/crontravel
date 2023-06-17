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
    Review
)


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
    list_display = (
        'id',
        'name',
        'price',
        'children_age',
        'price_children',
        'description',
        'author',
        'slug',
        'gathering_place',
        'company',
        'type_excursion',
        'transport',
        'size_group',
        'starting_point',
        'city',
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
    )
    list_filter = (
        'excursion',
        'score',
    )
