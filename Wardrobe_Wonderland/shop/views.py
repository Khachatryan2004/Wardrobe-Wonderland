from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages, auth
from .models import *
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Count, Sum
from django.db.models import Q
from django.db.models.functions import Lower

from payment.models import OrderItem


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        men_sub_category_slug = self.request.GET.get('men_sub_category')
        women_sub_category_slug = self.request.GET.get('women_sub_category')
        clothing_type_men_slug = self.request.GET.get('clothing_type_men')
        clothing_type_women_slug = self.request.GET.get('clothing_type_women')
        shoes_type_men_slug = self.request.GET.get('shoes_type_men')
        shoes_type_women_slug = self.request.GET.get('shoes_type_women')
        accessories_type_men_slug = self.request.GET.get('accessories_type_men')
        accessories_type_women_slug = self.request.GET.get('accessories_type_women')
        dresses_type_women_slug = self.request.GET.get('dresses_type_women')
        selected_clothing_color = self.request.GET.get('clothing_color')
        selected_shoes_color = self.request.GET.get('shoes_color')
        selected_accessories_color = self.request.GET.get('accessories_color')
        selected_dresses_color = self.request.GET.get('dresses_color')
        selected_size_clothing = self.request.GET.get('size_clothing')
        selected_size_shoes = self.request.GET.get('size_shoes')
        selected_size_accessories = self.request.GET.get('size_accessories')
        selected_size_dresses = self.request.GET.get('size_dresses')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        ordering = self.request.GET.get('ordering')
        price_sort = self.request.GET.get('price_sort')

        queryset = queryset.filter(status=True)

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if men_sub_category_slug:
            queryset = queryset.filter(men_sub_category__slug=men_sub_category_slug)

        if women_sub_category_slug:
            queryset = queryset.filter(women_sub_category__slug=women_sub_category_slug)

        if clothing_type_men_slug:
            queryset = queryset.filter(clothing_type_men__slug=clothing_type_men_slug)

        if clothing_type_women_slug:
            queryset = queryset.filter(clothing_type_women__slug=clothing_type_women_slug)

        if shoes_type_men_slug:
            queryset = queryset.filter(shoes_type_men__slug=shoes_type_men_slug)

        if shoes_type_women_slug:
            queryset = queryset.filter(shoes_type_women__slug=shoes_type_women_slug)

        if accessories_type_men_slug:
            queryset = queryset.filter(accessories_type_men__slug=accessories_type_men_slug)

        if accessories_type_women_slug:
            queryset = queryset.filter(accessories_type_women__slug=accessories_type_women_slug)

        if dresses_type_women_slug:
            queryset = queryset.filter(dresses_type_women__slug=dresses_type_women_slug)

        if selected_clothing_color:
            queryset = queryset.filter(clothing_color=selected_clothing_color)

        if selected_shoes_color:
            queryset = queryset.filter(shoes_color=selected_shoes_color)

        if selected_accessories_color:
            queryset = queryset.filter(accessories_color=selected_accessories_color)

        if selected_dresses_color:
            queryset = queryset.filter(dresses_color=selected_dresses_color)

        if selected_size_clothing:
            queryset = queryset.filter(size_clothing=selected_size_clothing)

        if selected_size_shoes:
            queryset = queryset.filter(size_shoes=selected_size_shoes)

        if selected_size_accessories:
            queryset = queryset.filter(size_accessories=selected_size_accessories)

        if selected_size_dresses:
            queryset = queryset.filter(size_dresses=selected_size_dresses)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if ordering == 'name_az':
            queryset = queryset.annotate(lower_name=Lower('name')).order_by('lower_name')

        if ordering == 'name_za':
            queryset = queryset.annotate(lower_name=Lower('name')).order_by('-lower_name')

        if price_sort == 'low_to_high':
            queryset = queryset.order_by('price')

        if price_sort == 'high_to_low':
            queryset = queryset.order_by('-price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.get_queryset()
        # categories
        context['categories'] = Category.objects.filter(status=True)
        # sub categories
        context['men_sub_categories'] = MenSubCategory.objects.filter(status=True)
        context['women_sub_categories'] = WomenSubCategory.objects.filter(status=True)
        # types
        context['clothing_types_men'] = ClothingTypeMen.objects.filter(status=True)
        context['clothing_types_women'] = ClothingTypeWomen.objects.filter(status=True)
        context['shoes_types_men'] = ShoesTypeMen.objects.filter(status=True)
        context['shoes_types_women'] = ShoesTypeWomen.objects.filter(status=True)
        context['accessories_types_men'] = AccessoriesTypeMen.objects.filter(status=True)
        context['accessories_types_women'] = AccessoriesTypeWomen.objects.filter(status=True)
        context['dresses_types_women'] = DressesTypeWomen.objects.filter(status=True)
        # colors
        context['CLOTHING_COLOR'] = Item.CLOTHING_COLOR
        context['SHOES_COLOR'] = Item.SHOES_COLOR
        context['ACCESSORIES_COLOR'] = Item.ACCESSORIES_COLOR
        context['DRESSES_COLOR'] = Item.DRESSES_COLOR
        # sizes
        context['SIZE_CHOICES_CLOTHING'] = Item.SIZE_CHOICES_CLOTHING
        context['SIZE_CHOICES_SHOES'] = Item.SIZE_CHOICES_SHOES
        context['SIZE_CHOICES_ACCESSORIES'] = Item.SIZE_CHOICES_ACCESSORIES
        context['SIZE_CHOICES_DRESSES'] = Item.SIZE_CHOICES_DRESSES

        selected_category_slug = self.request.GET.get('category')
        selected_men_sub_category_slug = self.request.GET.get('men_sub_category')
        selected_women_sub_category_slug = self.request.GET.get('women_sub_category')

        if selected_category_slug:
            selected_category = get_object_or_404(Category, slug=selected_category_slug)
            context['selected_category'] = selected_category.name

        if selected_men_sub_category_slug:
            selected_men_sub_category = get_object_or_404(MenSubCategory, slug=selected_men_sub_category_slug)
            context['selected_men_sub_category'] = selected_men_sub_category.name

        if selected_women_sub_category_slug:
            selected_women_sub_category = get_object_or_404(WomenSubCategory, slug=selected_women_sub_category_slug)
            context['selected_women_sub_category'] = selected_women_sub_category.name

        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        total_purchased_count = OrderItem.objects.filter(item=item).aggregate(total_purchased_count=Sum('quantity'))[
                                    'total_purchased_count'] or 0
        context['total_purchased_count'] = total_purchased_count
        context['categories'] = Category.objects.filter(status=True)
        # colors
        context['CLOTHING_COLOR'] = Item.CLOTHING_COLOR
        context['SHOES_COLOR'] = Item.SHOES_COLOR
        context['ACCESSORIES_COLOR'] = Item.ACCESSORIES_COLOR
        context['DRESSES_COLOR'] = Item.DRESSES_COLOR
        # sizes
        context['SIZE_CHOICES_CLOTHING'] = Item.SIZE_CHOICES_CLOTHING
        context['SIZE_CHOICES_SHOES'] = Item.SIZE_CHOICES_SHOES
        context['SIZE_CHOICES_ACCESSORIES'] = Item.SIZE_CHOICES_ACCESSORIES
        context['SIZE_CHOICES_DRESSES'] = Item.SIZE_CHOICES_DRESSES

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


class Search(ListView):
    template_name = 'search_results.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        q = self.request.GET.get('q')
        return Item.objects.filter(Q(name__icontains=q) | Q(category__name__icontains=q))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context
