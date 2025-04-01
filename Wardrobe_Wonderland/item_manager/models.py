from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(TimeStampModel):
    name = models.CharField(max_length=20, unique=True)
    image = models.ImageField(upload_to='category_img/', null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class SubCategory(TimeStampModel):
    category = models.ManyToManyField(Category)
    subcategory = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.subcategory

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'


class Type(TimeStampModel):
    category = models.ManyToManyField(Category)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    type = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Type'
        verbose_name_plural = 'Types'


class Brand(TimeStampModel):
    subcategory = models.ManyToManyField(SubCategory)
    brand = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'


class Size(TimeStampModel):
    subcategory = models.ManyToManyField(SubCategory)
    size = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'


class Color(TimeStampModel):
    name = models.CharField(max_length=40, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'
