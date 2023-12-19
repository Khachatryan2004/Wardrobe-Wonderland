from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'status', 'get_photo',)
    list_display_links = ('name', 'get_photo')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")

    get_photo.short_description = 'Image'


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'status', 'get_photo',)
    list_display_links = ('name', 'get_photo',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")

    get_photo.short_description = 'Image'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'updated_at', 'status', 'get_photo', 'sub_category')
    list_display_links = ('name', 'get_photo',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('sub_category',)

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")

    get_photo.short_description = 'Image'


@admin.register(User)
class UserModelAdmin(UserAdmin):
    model = User

    fieldsets = (
        (('Personal info'), {'fields': (
            'username',
        )}),
        (('Permissions'), {'fields': (
            'is_active', 'is_staff', 'is_superuser',
        )}),
        (('Additional fields'), {'fields': (
            'date_joined',
            'password',
        )},),
        (('Stripe'), {'fields': (
            'stripe_customer_id', 'stripe_account_id'
        )},),

    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    readonly_fields = ('id',)
    list_display = ('id', 'username',)
    list_display_links = ('id', 'username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username',)
    ordering = ['-pk']
    list_per_page = 20
