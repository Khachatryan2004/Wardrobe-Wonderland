from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='category_img/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(TimeStampModel):
    name = models.CharField(max_length=40, unique=True)
    image = models.ImageField(upload_to='subcategory_img/')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'


class Item(TimeStampModel):
    name = models.CharField(max_length=40, unique=True)
    image = models.ImageField(upload_to='item_img/')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='sub_categories')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(_('First name'), max_length=30)
    last_name = models.CharField(_('Last name'), max_length=30)

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
