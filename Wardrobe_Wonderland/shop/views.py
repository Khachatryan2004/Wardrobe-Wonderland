from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib import messages, auth
from .forms import UserLoginForm, UserRegistrationForm, SearchForm, AddToFavoritesForm
from .models import *
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import stripe
import time
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class CategoryListView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'


class ItemListView(ListView):
    model = Item
    template_name = 'item_list.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        return Item.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = context['items']

        paginator = Paginator(items, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        context['items'] = items
        context['paginator'] = paginator
        context['page_obj'] = items
        context['is_paginated'] = True if paginator.num_pages > 1 else False

        return context


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_detail.html'
    context_object_name = 'item'


def view_cart(request):
    return render(request, 'cart.html')


def profile(request):
    return render(request, 'profile.html')


def cart_warning(request):
    return render(request, 'cart_warning.html')


def add_to_favorites(request):
    if request.method == 'POST':
        form = AddToFavoritesForm(request.POST)
        if form.is_valid():
            favorites = request.session.get('favorites', [])

            form.cleaned_data['price'] = float(form.cleaned_data['price'])

            favorites.append(form.cleaned_data)
            request.session['favorites'] = favorites
    return redirect('item_list')


def favorite(request):
    favorites = request.session.get('favorites', [])
    return render(request, 'favorites.html', {'favorites': favorites})


def remove_from_favorites(request):
    if request.method == 'POST':
        slug = request.POST.get('slug')
        if slug:
            favorites = request.session.get('favorites', [])
            updated_favorites = [item for item in favorites if item.get('slug') != slug]
            request.session['favorites'] = updated_favorites

    return redirect('favorites')


class Search(ListView):
    template_name = 'search_results.html'
    context_object_name = 'items'
    paginate_by = 5

    def get_queryset(self):
        return Item.objects.filter(name__icontains=self.request.GET.get('q'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        return context


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('category'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login_page'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'registration.html', context)

# <div class="row" data-aos="fade-up">
#               <div class="col-md-12 text-center">
#                 <div class="site-block-27">
#                   <ul>
#                     <li><a href="#">&lt;</a></li>
#                     <li class="active"><span>1</span></li>
#                     <li><a href="#">2</a></li>
#                     <li><a href="#">3</a></li>
#                     <li><a href="#">4</a></li>
#                     <li><a href="#">5</a></li>
#                     <li><a href="#">&gt;</a></li>
#                   </ul>
#                 </div>
#               </div>
#             </div>
#           </div>
