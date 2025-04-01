from decimal import Decimal
from shop.models import ItemProxy


class Cart():
    def __init__(self, request) -> None:
        """
            Initialize the shopping cart.

            Args:
                request: The request object containing information about the current web application request.
            """

        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def __len__(self):
        return sum(item.get('qty', 0) for item in self.cart.values())

    def __iter__(self):
        item_ids = self.cart.keys()
        items = ItemProxy.objects.filter(id__in=item_ids)
        cart = self.cart.copy()

        for item in items:
            cart[str(item.id)]['item'] = item

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def add(self, item, quantity=1, color=None, size=None, brand=None):
        """
        Add an item to cart.

        Args:
           item: The item to be added to cart.
           color: The selected color of the item.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            price = item.get_discounted_price() if item.discount else item.price
            self.cart[item_id] = {'qty': quantity, 'price': str(price), 'color': color, 'size': size, 'brand':brand}
        else:
            self.cart[item_id]['qty'] += quantity
            self.cart[item_id]['color'] = color
            self.cart[item_id]['size'] = size
            self.cart[item_id]['brand'] = brand

        self.session.modified = True

    def delete(self, item):
        """
        Delete an item from cart.

        Args:
            item_id: The ID of the item to be removed from cart.
        """
        item_id = str(item)
        if item_id in self.cart:
            del self.cart[item_id]
            self.session.modified = True

    def update(self, item, quantity):
        item_id = str(item)
        if item_id in self.cart:
            self.cart[item_id]['qty'] = quantity
            self.session.modified = True

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
