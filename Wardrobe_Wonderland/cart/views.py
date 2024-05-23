from django.shortcuts import render, get_object_or_404
from shop.models import Category, ItemProxy
from .cart import Cart
from django.http import JsonResponse


def cart_view(request):
    cart = Cart(request)
    categories = Category.objects.all()
    context = {
        'cart': cart,
        'categories': categories
    }
    return render(request, 'cart_view.html', context)


def cart_add(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))
        item_color = request.POST.get('item_color')
        item_size = request.POST.get('item_size')

        if not item_color or not item_size:
            return JsonResponse({'error': 'Please select size and color.'}, status=400)

        item = get_object_or_404(ItemProxy, id=item_id)

        cart.add(item=item, quantity=item_qty, color=item_color, size=item_size)

        cart_qty = cart.__len__()

        response = JsonResponse({'qty': cart_qty, 'item': item.name})

        return response


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        cart.delete(item=item_id)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()
        response = JsonResponse({'qty': cart_qty, 'total': cart_total})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        item_id = int(request.POST.get('item_id'))
        item_qty = int(request.POST.get('item_qty'))

        cart.update(item=item_id, quantity=item_qty)
        cart_qty = cart.__len__()
        cart_total = cart.get_total_price()

        response = JsonResponse({'qty': cart_qty, 'total': cart_total})
        return response
