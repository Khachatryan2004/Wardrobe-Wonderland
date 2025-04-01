import uuid
import stripe
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.templatetags.static import static
from yookassa import Configuration, Payment
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse, Http404
from .models import *
from .forms import *
from cart.cart import Cart
from django.conf import settings
from forex_python.converter import CurrencyRates
import requests

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


@login_required(login_url='account:login')
def shipping(request):
    try:
        shipping_address = ShippingAddress.objects.get(user=request.user)
    except ShippingAddress.DoesNotExist:
        shipping_address = None

    form = ShippingAddressForm(instance=shipping_address)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipping_address)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()
            return redirect('account:dashboard')

    return render(request, 'shipping.html', {'form': form})


def checkout(request):
    if request.user.is_authenticated:
        shipping_address = ShippingAddress.objects.filter(user=request.user).first()
        if shipping_address:
            return render(request, 'checkout.html', {'shipping_address': shipping_address})
        else:
            return HttpResponseRedirect(reverse('payment:shipping'))

    return render(request, 'checkout.html')


def complete_order(request):
    if request.method == 'POST':
        payment_type = request.POST.get('stripe-payment', 'yookassa-payment')

        name = request.POST.get('name')
        email = request.POST.get('email')
        street_address = request.POST.get('street_address')
        apartment_address = request.POST.get('apartment_address')
        country = request.POST.get('country')
        zip = request.POST.get('zip')
        cart = Cart(request)
        total_price = cart.get_total_price()
        shipping_address, _ = ShippingAddress.objects.get_or_create(
            user=request.user,
            defaults={
                'name': name,
                'email': email,
                'street_address': street_address,
                'apartment_address': apartment_address,
                'country': country,
                'zip': zip
            }
        )

        match payment_type:
            case 'stripe-payment':
                session_data = {
                    'mode': 'payment',
                    'success_url': request.build_absolute_uri(reverse('payment:payment_success')),
                    'cancel_url': request.build_absolute_uri(reverse('payment:payment_failed')),
                    'line_items': []
                }

                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user, shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order, item=item['item'], price=item['price'], quantity=item['qty'],
                            color=item['color'], size=item['size'], user=request.user, brand=item['brand'])
                        UserOrder.objects.create(
                            order=order,
                            user=request.user,
                            item=item['item'],
                            quantity=item['qty'],
                            price=item['price'],
                            color=item['color'],
                            size=item['size'],
                            brand=item['brand']
                        )
                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['item'],
                                    'metadata': {
                                        'color': item['color'],
                                        'size': item['size'],
                                        'brand': item['brand']
                                    },
                                },
                            },
                            'quantity': item['qty']
                        })
                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)

                else:
                    order = Order.objects.create(shipping_address=shipping_address, amount=total_price)
                    for item in cart:
                        OrderItem.objects.create(
                            order=order, item=item['item'], price=item['price'], quantity=item['qty'],
                            color=item['color'], size=item['size'], brand=item['brand'])
                        UserOrder.objects.create(
                            order=order,
                            user=request.user,
                            item=item['item'],
                            quantity=item['qty'],
                            price=item['price'],
                            color=item['color'],
                            size=item['size'],
                            brand=item['brand']
                        )

                        session_data['line_items'].append({
                            'price_data': {
                                'unit_amount': int(item['price'] * Decimal(100)),
                                'currency': 'usd',
                                'name': item['item'],
                                'metadata': {
                                    'color': item['color'],
                                    'size': item['size'],
                                    'brand': item['brand']
                                },
                            },
                            'quantity': item['qty'],
                        })
                    session_data['client_reference_id'] = order.id
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)

            case "yookassa-payment":
                response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
                data = response.json()
                usd_to_rub_rate = data['rates']['RUB']
                total_price_usd = float(total_price)
                total_price_rub = total_price_usd * usd_to_rub_rate

                idempotence_key = uuid.uuid4()

                currency = 'RUB'
                description = 'Товары в корзине'
                payment = Payment.create({
                    "amount": {
                        "value": str(total_price_rub),
                        "currency": currency
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": request.build_absolute_uri(reverse('payment:payment_success')),
                    },
                    "capture": True,
                    "test": True,
                    "description": description,
                }, idempotence_key)

                confirmation_url = payment.confirmation.confirmation_url

                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user, shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order, item=item['item'], price=item['price'], quantity=item['qty'],
                            color=item['color'], size=item['size'], brand=item['brand'], user=request.user)
                        UserOrder.objects.create(
                            user=request.user,
                            item=item['item'],
                            quantity=item['qty'],
                            price=item['price'],
                            color=item['color'],
                            size=item['size'],
                            brand=item['brand']
                        )

                    return redirect(confirmation_url)

                else:
                    order = Order.objects.create(
                        shipping_address=shipping_address, amount=total_price)

                    for item in cart:
                        OrderItem.objects.create(
                            order=order, item=item['item'], price=item['price'], quantity=item['qty'],
                            color=item['color'], size=item['size'], brand=item['brand'])
                        UserOrder.objects.create(
                            order=order,
                            user=request.user,
                            item=item['item'],
                            quantity=item['qty'],
                            price=item['price'],
                            color=item['color'],
                            size=item['size'],
                            brand=item['brand']
                        )


@login_required
def user_orders(request):
    orders = UserOrder.objects.filter(user=request.user).select_related('item', 'order')
    total_cost = sum(order.price * order.quantity for order in orders)

    return render(request, 'dashboard/user_orders.html', {
        'orders': orders,
        'total_cost': total_cost,
    })


def payment_success(request):
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]
    return render(request, 'payment_success.html')


def payment_failed(request):
    return render(request, 'payment_failed.html')


@staff_member_required
def admin_order_pdf(request, order_id):
    try:
        order = Order.objects.select_related('user', 'shipping_address').get(id=order_id)
    except Order.DoesNotExist:
        raise Http404('Order not found')
    html = render_to_string('order/pdf/pdf_invoice.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
