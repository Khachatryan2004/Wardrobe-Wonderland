from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import *
from payment.models import *


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'updated_at', 'status', 'get_photo',)
#     list_display_links = ('name', 'get_photo')
#     list_editable = ('status',)
#     search_fields = ('name',)
#     prepopulated_fields = {'slug': ('name',)}
#
#     def get_photo(self, obj):
#         return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")
#
#     get_photo.short_description = 'Image'


@admin.register(MenSubCategory)
class MenSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'status',)
    list_display_links = ('name',)
    list_editable = ('status',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    # def get_photo(self, obj):
    #     return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")
    #
    # get_photo.short_description = 'Image'


@admin.register(WomenSubCategory)
class WomenSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'status',)
    list_display_links = ('name',)
    list_editable = ('status',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    # def get_photo(self, obj):
    #     return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")
    #
    # get_photo.short_description = 'Image'


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'price', 'discount', 'get_discounted_price', 'updated_at', 'brand', 'category',
        'subcategory', 'type', 'get_photo', 'status',)
    list_display_links = ('name', 'get_photo',)
    search_fields = ('name', 'category')
    list_editable = ('status',)
    filter_horizontal = ('color','size')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'subcategory__subcategory', 'brand__brand', 'color', 'type__type')

    # fieldsets = (
    #     ("Name and Slug", {
    #         "fields": (("name", "slug"),)}),
    #     (None, {
    #         "fields": ("shoes_type_women", "status", )
    #     })
    # )

    def get_photo(self, obj):
        return mark_safe(f"<img src={obj.image.url} width='65' height='40/>'")

    get_photo.short_description = 'Image'


@admin.register(ClothingTypeMen)
class ClothingTypeMenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    list_editable = ('status',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(ClothingTypeWomen)
class ClothingTypeWomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    list_editable = ('status',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(ShoesTypeMen)
class ShoesTypeMenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(ShoesTypeWomen)
class ShoesTypeWomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(AccessoriesTypeMen)
class AccessoriesTypeMenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(AccessoriesTypeWomen)
class AccessoriesTypeWomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


@admin.register(DressesTypeWomen)
class DressesTypeWomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated_at', 'status')
    list_display_links = ('name',)
    search_fields = ('name',)
    list_editable = ('status',)
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('name',)


class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    extra = 0


@admin.register(User)
class UserModelAdmin(UserAdmin):
    model = User

    fieldsets = (
        (('Personal info'), {'fields': (
            'username',
            'email'
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
    inlines = [ShippingAddressInline]

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    readonly_fields = ('id',)
    list_display = ('id', 'username', 'is_active')
    list_display_links = ('id', 'username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
    search_fields = ('username',)
    ordering = ['-pk']
    list_per_page = 20
