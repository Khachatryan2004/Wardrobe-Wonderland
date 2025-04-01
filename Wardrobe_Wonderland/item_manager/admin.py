from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'status', 'get_photo',)
    list_display_links = ('name', 'get_photo')
    list_editable = ('status',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")

    get_photo.short_description = 'Image'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory', 'created_at', 'updated_at', 'status',)
    list_display_links = ('subcategory',)
    list_editable = ('status',)
    list_filter = ('category',)
    filter_horizontal = ('category',)
    search_fields = ('subcategory',)
    prepopulated_fields = {'slug': ('subcategory',)}


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('type', 'created_at', 'updated_at', 'status', 'subcategory')
    list_display_links = ('type',)
    list_editable = ('status',)
    filter_horizontal = ('category',)
    search_fields = ('type', 'subcategory__subcategory',)
    list_filter = ('category', 'subcategory__subcategory',)
    prepopulated_fields = {'slug': ('subcategory', 'type',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'created_at', 'updated_at', 'status',)
    list_display_links = ('brand',)
    list_editable = ('status',)
    filter_horizontal = ('subcategory',)
    search_fields = ('brand', 'subcategory')
    list_filter = ('subcategory', 'brand')
    prepopulated_fields = {'slug': ('subcategory', 'brand',)}


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'created_at', 'updated_at', 'status', )
    list_display_links = ('size',)
    list_editable = ('status',)
    filter_horizontal = ('subcategory',)
    search_fields = ('size', 'subcategory',)
    list_filter = ('subcategory',)
    prepopulated_fields = {'slug': ('size',)}


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at', 'status',)
    list_display_links = ('name',)
    list_editable = ('status',)
    search_fields = ('name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
