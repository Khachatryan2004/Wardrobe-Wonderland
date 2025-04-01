from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages, auth
from .models import *
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Count, Sum
from django.db.models import F, Q, FloatField, ExpressionWrapper, Max, Min, DecimalField
from django.db.models.functions import Lower
from item_manager.models import *


from payment.models import OrderItem


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'


class ItemListView(ListView):
    # model = Item
    # template_name = 'item_list.html'
    model = ItemProxy
    context_object_name = 'items'
    paginate_by = 15

    def get_template_names(self):
        if self.request.htmx:
            return "components/item_list.html"
        return "item_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        subcategory_slug = self.request.GET.get('subcategory')
        type_slug = self.request.GET.get('type')
        size_slug = self.request.GET.get('size')
        brand_slug = self.request.GET.get('brand')
        color_slug = self.request.GET.get('color')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        ordering = self.request.GET.get('ordering')
        discount_range = self.request.GET.get('discount')
        q = self.request.GET.get('q')

        queryset = queryset.filter(status=True)

        if q:
            queryset = queryset.filter(Q(name__icontains=q) | Q(category__name__icontains=q))

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)

        if type_slug:
            queryset = queryset.filter(type__slug=type_slug)

        if size_slug:
            queryset = queryset.filter(size__slug=size_slug)

        if brand_slug:
            queryset = queryset.filter(brand__slug=brand_slug)

        if color_slug:
            queryset = queryset.filter(color__slug=color_slug)

        if min_price:
            queryset = queryset.annotate(discounted_price=ExpressionWrapper(
                F('price') - (F('price') * F('discount') / 100),
                output_field=FloatField()
            ))
            queryset = queryset.filter(Q(price__gte=min_price) | Q(discounted_price__gte=min_price))

        if max_price:
            queryset = queryset.annotate(discounted_price=ExpressionWrapper(
                F('price') - (F('price') * F('discount') / 100),
                output_field=FloatField()
            ))
            queryset = queryset.filter(Q(price__lte=max_price) | Q(discounted_price__lte=max_price))

        if ordering:
            if ordering == 'name_az':
                queryset = queryset.annotate(lower_name=Lower('name')).order_by('lower_name')

            elif ordering == 'name_za':
                queryset = queryset.annotate(lower_name=Lower('name')).order_by('-lower_name')

            elif ordering == 'newest':
                queryset = queryset.order_by('updated_at')

            elif ordering == 'oldest':
                queryset = queryset.order_by('-updated_at')

            elif ordering == 'low_to_high':
                queryset = queryset.order_by('price')

            elif ordering == 'high_to_low':
                queryset = queryset.order_by('-price')

        if discount_range:
            if discount_range == 'up_to_20':
                queryset = queryset.filter(discount__lte=20)
            elif discount_range == '20_to_30':
                queryset = queryset.filter(discount__gt=20, discount__lte=30)
            elif discount_range == '30_to_40':
                queryset = queryset.filter(discount__gt=30, discount__lte=40)
            elif discount_range == '40_to_50':
                queryset = queryset.filter(discount__gt=40, discount__lte=50)
            elif discount_range == '50_to_60':
                queryset = queryset.filter(discount__gt=50, discount__lte=60)
            elif discount_range == '60_or_more':
                queryset = queryset.filter(discount__gt=60)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_queryset()
        context['categories'] = Category.objects.filter(status=True)
        context['colors'] = Color.objects.filter(status=True)

        selected_category_slug = self.request.GET.get('category')
        selected_subcategory_slug = self.request.GET.get('subcategory')
        selected_type_slug = self.request.GET.get('type')
        selected_size_slug = self.request.GET.get('size')
        selected_brand_slug = self.request.GET.get('brand')
        selected_color_slug = self.request.GET.get('color')

        items = self.get_queryset()

        if selected_category_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug)
            context['selected_category'] = selected_category
            context['subcategories'] = SubCategory.objects.filter(category=selected_category, status=True)
            items = items.filter(category=selected_category)

        if selected_subcategory_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug)
            selected_subcategory = get_object_or_404(SubCategory, slug=selected_subcategory_slug)
            context['selected_subcategory'] = selected_subcategory
            context['types'] = Type.objects.filter(category=selected_category, subcategory=selected_subcategory,
                                                   status=True)
            context['sizes'] = Size.objects.filter(subcategory=selected_subcategory, status=True)
            context['brands'] = Brand.objects.filter(subcategory=selected_subcategory, status=True)
            items = items.filter(subcategory=selected_subcategory)

        if selected_type_slug:
            selected_type = get_object_or_404(Type, slug=selected_type_slug)
            context['selected_type'] = selected_type
            items = items.filter(type=selected_type)

        if selected_size_slug:
            selected_size = get_object_or_404(Size, slug=selected_size_slug)
            context['selected_size'] = selected_size
            items = items.filter(size=selected_size)

        if selected_brand_slug:
            selected_brand = get_object_or_404(Brand, slug=selected_brand_slug)
            context['selected_brand'] = selected_brand
            items = items.filter(brand=selected_brand)

        if selected_color_slug:
            selected_color = get_object_or_404(Color, slug=selected_color_slug)
            context['selected_color'] = selected_color
            items = items.filter(color=selected_color)

        min_discounted_price = items.aggregate(min_price=Min(F('price') - F('price') * F('discount') / 100,
                                                             output_field=DecimalField()))['min_price']
        max_discounted_price = items.aggregate(max_price=Max(F('price') - F('price') * F('discount') / 100,
                                                             output_field=DecimalField()))['max_price']

        if min_discounted_price is None:
            min_discounted_price = items.aggregate(min_price=Min('price'))['min_price']
        if max_discounted_price is None:
            max_discounted_price = items.aggregate(max_price=Max('price'))['max_price']

        context['min_price'] = min_discounted_price if min_discounted_price is not None else 0
        context['max_price'] = max_discounted_price if max_discounted_price is not None else 0

        return context


class ItemDetailView(DetailView):
    model = ItemProxy
    template_name = 'item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        total_purchased_count = OrderItem.objects.filter(item=item).aggregate(total_purchased_count=Sum('quantity'))[
                                    'total_purchased_count'] or 0
        context['total_purchased_count'] = total_purchased_count
        context['categories'] = Category.objects.filter(status=True)
        context['colors'] = item.color.all()
        context['sizes'] = item.size.all()
        # colors
        # context['CLOTHING_COLOR'] = Item.CLOTHING_COLOR
        # context['SHOES_COLOR'] = Item.SHOES_COLOR
        # context['ACCESSORIES_COLOR'] = Item.ACCESSORIES_COLOR
        # context['DRESSES_COLOR'] = Item.DRESSES_COLOR
        # sizes
        context['SIZE_CHOICES_CLOTHING'] = Item.SIZE_CHOICES_CLOTHING
        context['SIZE_CHOICES_SHOES'] = Item.SIZE_CHOICES_SHOES
        context['SIZE_CHOICES_ACCESSORIES'] = Item.SIZE_CHOICES_ACCESSORIES
        context['SIZE_CHOICES_DRESSES'] = Item.SIZE_CHOICES_DRESSES

        return context

    def review(self, request, *args, **kwargs):
        self.object = self.get_object()
        item = self.object

        if request.user.is_authenticated:
            if item.reviews.filter(created_by=request.user).exists():
                messages.error(request, 'You have already made a review for this product.')
            else:
                rating = request.POST.get('rating', 3)
                content = request.POST.get('content', '')
                if content:
                    item.reviews.create(rating=rating, content=content, created_by=request.user, item=item)
                    return redirect(request.path)
        else:
            messages.error(request, 'You need to be logged in to make a review.')

        context = super().get_context_data(**kwargs)
        return self.render_to_response(context)


class Search(ItemListView):
    template_name = 'item_list.html'
    context_object_name = 'search'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        queryset = Item.objects.filter(Q(name__icontains=q) | Q(category__name__icontains=q))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def cart_warning(request):
    return render(request, 'cart_warning.html')


# def add_to_favorites(request):
#     if request.method == 'POST':
#         form = AddToFavoritesForm(request.POST)
#         if form.is_valid():
#             favorites = request.session.get('favorites', [])
#
#             form.cleaned_data['price'] = float(form.cleaned_data['price'])
#
#             favorites.append(form.cleaned_data)
#             request.session['favorites'] = favorites
#     return redirect('item_list')


# def favorite(request):
#     favorites = request.session.get('favorites', [])
#     categories = Category.objects.filter(status=True)
#     return render(request, 'favorites.html', {'favorites': favorites, 'categories': categories})


# def remove_from_favorites(request):
#     if request.method == 'POST':
#         slug = request.POST.get('slug')
#         if slug:
#             favorites = request.session.get('favorites', [])
#             updated_favorites = [item for item in favorites if item.get('slug') != slug]
#             request.session['favorites'] = updated_favorites
#
#     return redirect('favorites')



# class ItemListView(ListView):
#     # model = Item
#     # template_name = 'item_list.html'
#     model = ItemProxy
#     context_object_name = 'items'
#     paginate_by = 15
#
#     def get_template_names(self):
#         if self.request.htmx:
#             return "components/item_list.html"
#         return "item_list.html"
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category_slug = self.request.GET.get('category')
#         men_sub_category_slug = self.request.GET.get('men_sub_category')
#         women_sub_category_slug = self.request.GET.get('women_sub_category')
#         clothing_type_men_slug = self.request.GET.get('clothing_type_men')
#         clothing_type_women_slug = self.request.GET.get('clothing_type_women')
#         shoes_type_men_slug = self.request.GET.get('shoes_type_men')
#         shoes_type_women_slug = self.request.GET.get('shoes_type_women')
#         accessories_type_men_slug = self.request.GET.get('accessories_type_men')
#         accessories_type_women_slug = self.request.GET.get('accessories_type_women')
#         dresses_type_women_slug = self.request.GET.get('dresses_type_women')
#         selected_clothing_color = self.request.GET.get('clothing_color')
#         selected_shoes_color = self.request.GET.get('shoes_color')
#         selected_accessories_color = self.request.GET.get('accessories_color')
#         selected_dresses_color = self.request.GET.get('dresses_color')
#         selected_size_clothing = self.request.GET.get('size_clothing')
#         selected_size_shoes = self.request.GET.get('size_shoes')
#         selected_size_accessories = self.request.GET.get('size_accessories')
#         selected_size_dresses = self.request.GET.get('size_dresses')
#         min_price = self.request.GET.get('min_price')
#         max_price = self.request.GET.get('max_price')
#         ordering = self.request.GET.get('ordering')
#         price_sort = self.request.GET.get('price_sort')
#
#         queryset = queryset.filter(status=True)
#
#         if category_slug:
#             queryset = queryset.filter(category__slug=category_slug)
#
#         if men_sub_category_slug:
#             queryset = queryset.filter(men_sub_category__slug=men_sub_category_slug)
#
#         if women_sub_category_slug:
#             queryset = queryset.filter(women_sub_category__slug=women_sub_category_slug)
#
#         if clothing_type_men_slug:
#             queryset = queryset.filter(clothing_type_men__slug=clothing_type_men_slug)
#
#         if clothing_type_women_slug:
#             queryset = queryset.filter(clothing_type_women__slug=clothing_type_women_slug)
#
#         if shoes_type_men_slug:
#             queryset = queryset.filter(shoes_type_men__slug=shoes_type_men_slug)
#
#         if shoes_type_women_slug:
#             queryset = queryset.filter(shoes_type_women__slug=shoes_type_women_slug)
#
#         if accessories_type_men_slug:
#             queryset = queryset.filter(accessories_type_men__slug=accessories_type_men_slug)
#
#         if accessories_type_women_slug:
#             queryset = queryset.filter(accessories_type_women__slug=accessories_type_women_slug)
#
#         if dresses_type_women_slug:
#             queryset = queryset.filter(dresses_type_women__slug=dresses_type_women_slug)
#
#         if selected_clothing_color:
#             queryset = queryset.filter(clothing_color=selected_clothing_color)
#
#         if selected_shoes_color:
#             queryset = queryset.filter(shoes_color=selected_shoes_color)
#
#         if selected_accessories_color:
#             queryset = queryset.filter(accessories_color=selected_accessories_color)
#
#         if selected_dresses_color:
#             queryset = queryset.filter(dresses_color=selected_dresses_color)
#
#         if selected_size_clothing:
#             queryset = queryset.filter(size_clothing=selected_size_clothing)
#
#         if selected_size_shoes:
#             queryset = queryset.filter(size_shoes=selected_size_shoes)
#
#         if selected_size_accessories:
#             queryset = queryset.filter(size_accessories=selected_size_accessories)
#
#         if selected_size_dresses:
#             queryset = queryset.filter(size_dresses=selected_size_dresses)
#
#         if min_price:
#             queryset = queryset.filter(price__gte=min_price)
#
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#
#         if ordering == 'name_az':
#             queryset = queryset.annotate(lower_name=Lower('name')).order_by('lower_name')
#
#         if ordering == 'name_za':
#             queryset = queryset.annotate(lower_name=Lower('name')).order_by('-lower_name')
#
#         if price_sort == 'low_to_high':
#             queryset = queryset.order_by('price')
#
#         if price_sort == 'high_to_low':
#             queryset = queryset.order_by('-price')
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['items'] = self.get_queryset()
#         # categories
#         context['categories'] = Category.objects.filter(status=True)
#         # sub categories
#         context['men_sub_categories'] = MenSubCategory.objects.filter(status=True)
#         context['women_sub_categories'] = WomenSubCategory.objects.filter(status=True)
#         # types
#         context['clothing_types_men'] = ClothingTypeMen.objects.filter(status=True)
#         context['clothing_types_women'] = ClothingTypeWomen.objects.filter(status=True)
#         context['shoes_types_men'] = ShoesTypeMen.objects.filter(status=True)
#         context['shoes_types_women'] = ShoesTypeWomen.objects.filter(status=True)
#         context['accessories_types_men'] = AccessoriesTypeMen.objects.filter(status=True)
#         context['accessories_types_women'] = AccessoriesTypeWomen.objects.filter(status=True)
#         context['dresses_types_women'] = DressesTypeWomen.objects.filter(status=True)
#         # colors
#         context['CLOTHING_COLOR'] = Item.CLOTHING_COLOR
#         context['SHOES_COLOR'] = Item.SHOES_COLOR
#         context['ACCESSORIES_COLOR'] = Item.ACCESSORIES_COLOR
#         context['DRESSES_COLOR'] = Item.DRESSES_COLOR
#         # sizes
#         context['SIZE_CHOICES_CLOTHING'] = Item.SIZE_CHOICES_CLOTHING
#         context['SIZE_CHOICES_SHOES'] = Item.SIZE_CHOICES_SHOES
#         context['SIZE_CHOICES_ACCESSORIES'] = Item.SIZE_CHOICES_ACCESSORIES
#         context['SIZE_CHOICES_DRESSES'] = Item.SIZE_CHOICES_DRESSES
#
#         selected_category_slug = self.request.GET.get('category')
#         selected_men_sub_category_slug = self.request.GET.get('men_sub_category')
#         selected_women_sub_category_slug = self.request.GET.get('women_sub_category')
#
#         if selected_category_slug:
#             selected_category = get_object_or_404(Category, slug=selected_category_slug)
#             context['selected_category'] = selected_category.name
#
#         if selected_men_sub_category_slug:
#             selected_men_sub_category = get_object_or_404(MenSubCategory, slug=selected_men_sub_category_slug)
#             context['selected_men_sub_category'] = selected_men_sub_category.name
#
#         if selected_women_sub_category_slug:
#             selected_women_sub_category = get_object_or_404(WomenSubCategory, slug=selected_women_sub_category_slug)
#             context['selected_women_sub_category'] = selected_women_sub_category.name
#
#         return context


# class ItemDetailView(DetailView):
#     model = ItemProxy
#     template_name = 'item_detail.html'
#     context_object_name = 'item'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         item = self.object
#         total_purchased_count = OrderItem.objects.filter(item=item).aggregate(total_purchased_count=Sum('quantity'))[
#                                     'total_purchased_count'] or 0
#         context['total_purchased_count'] = total_purchased_count
#         context['categories'] = Category.objects.filter(status=True)
#         # colors
#         context['CLOTHING_COLOR'] = Item.CLOTHING_COLOR
#         context['SHOES_COLOR'] = Item.SHOES_COLOR
#         context['ACCESSORIES_COLOR'] = Item.ACCESSORIES_COLOR
#         context['DRESSES_COLOR'] = Item.DRESSES_COLOR
#         # sizes
#         context['SIZE_CHOICES_CLOTHING'] = Item.SIZE_CHOICES_CLOTHING
#         context['SIZE_CHOICES_SHOES'] = Item.SIZE_CHOICES_SHOES
#         context['SIZE_CHOICES_ACCESSORIES'] = Item.SIZE_CHOICES_ACCESSORIES
#         context['SIZE_CHOICES_DRESSES'] = Item.SIZE_CHOICES_DRESSES
#
#         return context
#
#     def review(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         item = self.object
#
#         if request.user.is_authenticated:
#             if item.reviews.filter(created_by=request.user).exists():
#                 messages.error(request, 'You have already made a review for this product.')
#             else:
#                 rating = request.POST.get('rating', 3)
#                 content = request.POST.get('content', '')
#                 if content:
#                     item.reviews.create(rating=rating, content=content, created_by=request.user, item=item)
#                     return redirect(request.path)
#         else:
#             messages.error(request, 'You need to be logged in to make a review.')
#
#         context = super().get_context_data(**kwargs)
#         return self.render_to_response(context)
