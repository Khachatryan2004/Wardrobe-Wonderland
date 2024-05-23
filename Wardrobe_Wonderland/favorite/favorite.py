# from shop.models import ItemProxy
# from decimal import Decimal
#
#
# class Favorite():
#     def __init__(self, request) -> None:
#         """
#         Initialize the favorites.
#
#         Args:
#             request: The request object containing information about the current web application request.
#         """
#
#         self.session = request.session
#
#         favorite = self.session.get('session_key')
#
#         if not favorite:
#             favorite = self.session['session_key'] = {}
#
#         self.favorite = favorite
#
#     def __iter__(self):
#         """
#         Allow iteration over favorite items.
#         """
#         item_ids = self.favorite.keys()
#         items = ItemProxy.objects.filter(id__in=item_ids)
#         favorite = self.favorite.copy()
#
#         for item in items:
#             favorite[str(item.id)]['item'] = item
#
#         for item in favorite.values():
#             yield item
#
#     def add(self, item):
#         """
#         Add an item to favorites.
#
#         Args:
#             item: The item to be added to favorites.
#         """
#         item_id = str(item.id)
#         if item_id not in self.favorite:
#             self.favorite[item_id] = {'price': str(item.price)}
#
#         self.favorite[item_id]['price'] = str(item.price)
#         self.session.modified = True
#
#     def delete(self, item):
#         """
#         Delete an item from favorites.
#
#         Args:
#             item_id: The ID of the item to be removed from favorites.
#         """
#         item_id = str(item)
#         if item_id in self.favorite:
#             del self.favorite[item_id]
#             self.session.modified = True
#
#     def get_favorites(self):
#         """
#         Get all items from favorites.
#
#         Returns:
#             A dictionary containing all items in favorites.
#         """
#         return self.session.get('favorites', {})
