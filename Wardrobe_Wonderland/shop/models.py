from django.contrib.auth.models import AbstractUser, Permission, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from item_manager.models import *


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


# class Category(TimeStampModel):
#     name = models.CharField(max_length=20, unique=True)
#     image = models.ImageField(upload_to='category_img/', null=True, blank=True)
#     slug = models.SlugField(unique=True)
#
#     def __str__(self):
#         return self.name
#
#     class Meta:
#         verbose_name = 'Category'
#         verbose_name_plural = 'Categories'


class MenSubCategory(TimeStampModel):
    name = models.CharField(max_length=40, unique=True)
    # image = models.ImageField(upload_to='subcategory_img/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Men Sub Category '
        verbose_name_plural = 'Men Sub Categories'


class WomenSubCategory(TimeStampModel):
    name = models.CharField(max_length=40, unique=True)
    # image = models.ImageField(upload_to='subcategory_img/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Women Sub Category '
        verbose_name_plural = 'Women Sub Categories'


class ClothingTypeMen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Clothing Type Men'
        verbose_name_plural = 'Clothing Type Men'


class ClothingTypeWomen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Clothing Type Women'
        verbose_name_plural = 'Clothing Type Women'


class ShoesTypeMen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shoes Type Men'
        verbose_name_plural = 'Shoes Type Men'


class ShoesTypeWomen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Shoes Type Women'
        verbose_name_plural = 'Shoes Type Women'


class AccessoriesTypeMen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Accessories Type Men'
        verbose_name_plural = 'Accessories Type Men'


class AccessoriesTypeWomen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Accessories Type Women'
        verbose_name_plural = 'Accessories Type Women'


class DressesTypeWomen(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dresses Type Women'
        verbose_name_plural = 'Dresses Type Women'


class Item(TimeStampModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    image = models.ImageField(upload_to='item_img/', default='item_img/cloth_3.jpg', )
    image2 = models.ImageField(upload_to='item_img/', null=True, blank=True)
    image3 = models.ImageField(upload_to='item_img/', null=True, blank=True)
    image4 = models.ImageField(upload_to='item_img/', null=True, blank=True)
    image5 = models.ImageField(upload_to='item_img/', null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='subcategories', default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brands', default=1)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='types', default=1)
    color = models.ManyToManyField(Color, related_name='colors')
    size = models.ManyToManyField(Size, related_name='sizes',)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    description = models.TextField(null=True)

    SIZE_CHOICES_CLOTHING = [
        ('XS', 'XS (US 2 / UK 4 / Europe 32)'),
        ('S', 'S (US 4 / UK 6 / Europe 34)'),
        ('M', 'M (US 6 / UK 8 / Europe 36)'),
        ('L', 'L (US 8 / UK 10 / Europe 38)'),
        ('XL', 'XL (US 10 / UK 12 / Europe 40)'),
    ]

    size_clothing = models.CharField(max_length=30, choices=SIZE_CHOICES_CLOTHING, blank=True, null=True)

    SIZE_CHOICES_SHOES = [
        ('5 3 35', 'US 5 / UK 3 / Europe 35'),
        ('6 4 36', 'US 6 / UK 4 / Europe 36'),
        ('7 5 37', 'US 7 / UK 5 / Europe 37'),
        ('8 6 38', 'US 8 / UK 6 / Europe 38'),
        ('9 7 39', 'US 9 / UK 7 / Europe 39'),
        ('10 8 40', 'US 10 / UK 8 / Europe 40'),
        ('11 9 41', 'US 11 / UK 9 / Europe 41'),
        ('12 10 42', 'US 12 / UK 10 / Europe 42'),
        ('13 11 43', 'US 13 / UK 11 / Europe 43'),
        ('14 12 44', 'US 14 / UK 12 / Europe 44'),
    ]

    size_shoes = models.CharField(max_length=10, choices=SIZE_CHOICES_SHOES, blank=True, null=True)

    SIZE_CHOICES_ACCESSORIES = [
        ('One Size', 'One Size'),
        ('No Size', 'No Size'),
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    size_accessories = models.CharField(max_length=20, choices=SIZE_CHOICES_ACCESSORIES, blank=True, null=True)

    SIZE_CHOICES_DRESSES = [
        ('XS', 'XS (US 2 / UK 4 / Europe 32)'),
        ('S', 'S (US 4 / UK 6 / Europe 34)'),
        ('M', 'M (US 6 / UK 8 / Europe 36)'),
        ('L', 'L (US 8 / UK 10 / Europe 38)'),
        ('XL', 'XL (US 10 / UK 12 / Europe 40)'),
    ]

    size_dresses = models.CharField(max_length=40, choices=SIZE_CHOICES_DRESSES, blank=True, null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}"

    def get_discounted_price(self):
        """
        Calculates the discounted price based on the product's price and discount.

        Returns:
            decimal.Decimal: The discounted price.
        """
        discounted_price = self.price - (self.price * self.discount / 100)
        return round(discounted_price, 2)

    @property
    def full_image_url(self):
        """
        Returns:
            str: The full image URL.
        """
        return self.image.url if self.image else ''


class User(AbstractUser):
    is_active = models.BooleanField("active", default=True)
    stripe_customer_id = models.CharField(null=True, blank=True, max_length=255)

    stripe_account_id = models.CharField(blank=True, null=True, max_length=256)

    created_at = models.DateTimeField(_("Creation Time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Update Time"), auto_now=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='user_groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_permissions',
    )


class ItemManager(models.Manager):
    def get_queryset(self):
        """
        Returns a queryset of items that are available.

        Returns:
            QuerySet: A queryset of items that are available.
        """
        return super(ItemManager, self).get_queryset().filter(status=True)


class ItemProxy(Item):
    objects = ItemManager()

    class Meta:
        proxy = True

# class Item(TimeStampModel):
#     name = models.CharField(max_length=40, unique=True)
#     image = models.ImageField(upload_to='item_img/',  default='item_img/cloth_3.jpg', null=True, blank=True)
#     slug = models.SlugField(unique=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.IntegerField(
#         default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
#     men_sub_category = models.ForeignKey(MenSubCategory, on_delete=models.CASCADE, related_name='men_sub_categories',
#                                          blank=True,
#                                          null=True)
#     women_sub_category = models.ForeignKey(WomenSubCategory, on_delete=models.CASCADE,
#                                            related_name='women_sub_categories',
#                                            blank=True,
#                                            null=True)
#     description = models.TextField(null=True)
#     clothing_type_men = models.ForeignKey(ClothingTypeMen, on_delete=models.CASCADE, related_name='clothing_types_men',
#                                           blank=True,
#                                           null=True)
#     clothing_type_women = models.ForeignKey(ClothingTypeWomen, on_delete=models.CASCADE,
#                                             related_name='clothing_types_women',
#                                             blank=True,
#                                             null=True)
#     shoes_type_men = models.ForeignKey(ShoesTypeMen, on_delete=models.CASCADE, related_name='shoes_types_men',
#                                        blank=True,
#                                        null=True)
#     shoes_type_women = models.ForeignKey(ShoesTypeWomen, on_delete=models.CASCADE, related_name='shoes_types_women',
#                                          blank=True,
#                                          null=True)
#     accessories_type_men = models.ForeignKey(AccessoriesTypeMen, on_delete=models.CASCADE,
#                                              related_name='accessories_types_men',
#                                              blank=True,
#                                              null=True)
#     accessories_type_women = models.ForeignKey(AccessoriesTypeWomen, on_delete=models.CASCADE,
#                                                related_name='accessories_types_women',
#                                                blank=True,
#                                                null=True)
#     dresses_type_women = models.ForeignKey(DressesTypeWomen, on_delete=models.CASCADE,
#                                            related_name='dresses_types_women',
#                                            blank=True,
#                                            null=True)
#
#     SIZE_CHOICES_CLOTHING = [
#         ('XS', 'XS (US 2 / UK 4 / Europe 32)'),
#         ('S', 'S (US 4 / UK 6 / Europe 34)'),
#         ('M', 'M (US 6 / UK 8 / Europe 36)'),
#         ('L', 'L (US 8 / UK 10 / Europe 38)'),
#         ('XL', 'XL (US 10 / UK 12 / Europe 40)'),
#     ]
#
#     size_clothing = models.CharField(max_length=30, choices=SIZE_CHOICES_CLOTHING, blank=True, null=True)
#
#     SIZE_CHOICES_SHOES = [
#         ('5 3 35', 'US 5 / UK 3 / Europe 35'),
#         ('6 4 36', 'US 6 / UK 4 / Europe 36'),
#         ('7 5 37', 'US 7 / UK 5 / Europe 37'),
#         ('8 6 38', 'US 8 / UK 6 / Europe 38'),
#         ('9 7 39', 'US 9 / UK 7 / Europe 39'),
#         ('10 8 40', 'US 10 / UK 8 / Europe 40'),
#         ('11 9 41', 'US 11 / UK 9 / Europe 41'),
#         ('12 10 42', 'US 12 / UK 10 / Europe 42'),
#         ('13 11 43', 'US 13 / UK 11 / Europe 43'),
#         ('14 12 44', 'US 14 / UK 12 / Europe 44'),
#     ]
#
#     size_shoes = models.CharField(max_length=10, choices=SIZE_CHOICES_SHOES, blank=True, null=True)
#
#     SIZE_CHOICES_ACCESSORIES = [
#         ('One Size', 'One Size'),
#         ('No Size', 'No Size'),
#         ('XS', 'Extra Small'),
#         ('S', 'Small'),
#         ('M', 'Medium'),
#         ('L', 'Large'),
#         ('XL', 'Extra Large'),
#     ]
#
#     size_accessories = models.CharField(max_length=20, choices=SIZE_CHOICES_ACCESSORIES, blank=True, null=True)
#
#     SIZE_CHOICES_DRESSES = [
#         ('XS', 'XS (US 2 / UK 4 / Europe 32)'),
#         ('S', 'S (US 4 / UK 6 / Europe 34)'),
#         ('M', 'M (US 6 / UK 8 / Europe 36)'),
#         ('L', 'L (US 8 / UK 10 / Europe 38)'),
#         ('XL', 'XL (US 10 / UK 12 / Europe 40)'),
#     ]
#
#     size_dresses = models.CharField(max_length=40, choices=SIZE_CHOICES_DRESSES, blank=True, null=True)
#
#     CLOTHING_COLOR = [
#         ('RED', 'Red'),
#         ('BLUE', 'Blue'),
#         ('GREEN', 'Green'),
#         ('BLACK', 'Black'),
#         ('WHITE', 'White'),
#         ('YELLOW', 'Yellow'),
#         ('PURPLE', 'Purple'),
#         ('PINK', 'Pink'),
#         ('ORANGE', 'Orange'),
#         ('BROWN', 'Brown'),
#         ('GRAY', 'Gray'),
#         ('NAVY', 'Navy'),
#         ('TURQUOISE', 'Turquoise'),
#         ('SILVER', 'Silver'),
#         ('GOLD', 'Gold'),
#     ]
#
#     clothing_color = models.CharField(max_length=20, choices=CLOTHING_COLOR, blank=True, null=True)
#
#     SHOES_COLOR = [
#         ('RED', 'Red'),
#         ('BLUE', 'Blue'),
#         ('GREEN', 'Green'),
#         ('BLACK', 'Black'),
#         ('WHITE', 'White'),
#         ('YELLOW', 'Yellow'),
#         ('PURPLE', 'Purple'),
#         ('PINK', 'Pink'),
#         ('ORANGE', 'Orange'),
#         ('BROWN', 'Brown'),
#         ('GRAY', 'Gray'),
#         ('NAVY', 'Navy'),
#         ('TURQUOISE', 'Turquoise'),
#         ('SILVER', 'Silver'),
#         ('GOLD', 'Gold'),
#     ]
#
#     shoes_color = models.CharField(max_length=20, choices=SHOES_COLOR, blank=True, null=True)
#
#     ACCESSORIES_COLOR = [
#         ('RED', 'Red'),
#         ('BLUE', 'Blue'),
#         ('GREEN', 'Green'),
#         ('BLACK', 'Black'),
#         ('WHITE', 'White'),
#         ('YELLOW', 'Yellow'),
#         ('PURPLE', 'Purple'),
#         ('PINK', 'Pink'),
#         ('ORANGE', 'Orange'),
#         ('BROWN', 'Brown'),
#         ('GRAY', 'Gray'),
#         ('NAVY', 'Navy'),
#         ('TURQUOISE', 'Turquoise'),
#         ('SILVER', 'Silver'),
#         ('GOLD', 'Gold'),
#     ]
#
#     accessories_color = models.CharField(max_length=20, choices=ACCESSORIES_COLOR, blank=True, null=True)
#
#     DRESSES_COLOR = [
#         ('RED', 'Red'),
#         ('BLUE', 'Blue'),
#         ('GREEN', 'Green'),
#         ('BLACK', 'Black'),
#         ('WHITE', 'White'),
#         ('YELLOW', 'Yellow'),
#         ('PURPLE', 'Purple'),
#         ('PINK', 'Pink'),
#         ('ORANGE', 'Orange'),
#         ('BROWN', 'Brown'),
#         ('GRAY', 'Gray'),
#         ('NAVY', 'Navy'),
#         ('TURQUOISE', 'Turquoise'),
#         ('SILVER', 'Silver'),
#         ('GOLD', 'Gold'),
#     ]
#
#     dresses_color = models.CharField(max_length=20, choices=DRESSES_COLOR, blank=True, null=True)
#
#     class Meta:
#         verbose_name = 'Item'
#         verbose_name_plural = 'Items'
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.name}"
#
#     def get_discounted_price(self):
#         """
#         Calculates the discounted price based on the product's price and discount.
#
#         Returns:
#             decimal.Decimal: The discounted price.
#         """
#         discounted_price = self.price - (self.price * self.discount / 100)
#         return round(discounted_price, 2)
#
#     @property
#     def full_image_url(self):
#         """
#         Returns:
#             str: The full image URL.
#         """
#         return self.image.url if self.image else ''
