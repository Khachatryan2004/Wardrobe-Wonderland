# from django.db import models
# from django.contrib.auth import get_user_model
# from shop.models import Item
# User = get_user_model()
#
#
# class Favorite(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     favorite_item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     date_added = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user}'s favorite: {self.favorite_item}"
