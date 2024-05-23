from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
# from .favorite import Favorite
from shop.models import Category, ItemProxy, Item
from .models import Favorite


# def favorite_view(request):
#     favorite = Favorite(request)
#     categories = Category.objects.all()
#     context = {
#         'favorite': favorite,
#         'categories': categories
#     }
#     return render(request, 'favorite_view.html', context)
#
#
# def favorite_add(request):
#     favorite = Favorite(request)
#     if request.POST.get('action') == 'post':
#         item_id = int(request.POST.get('item_id'))
#
#         item = get_object_or_404(ItemProxy, id=item_id)
#
#         favorite.add(item=item)
#
#         response = JsonResponse({'item': item.name})
#
#         return response
#
#
# def favorite_delete(request):
#     favorite = Favorite(request)
#     if request.POST.get('action') == 'post':
#         item_id = int(request.POST.get('item_id'))
#         favorite.delete(item=item_id)
#
#         response = JsonResponse({'success': True})
#
#         return response
