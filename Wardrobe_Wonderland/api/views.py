from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from recommend.models import Review
from shop.models import Item
from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOrReadOnly
from .serializers import ItemSerializer, ItemDetailSerializer, ReviewSerializer

User = get_user_model()


class ItemListApiView(generics.ListAPIView):
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination
    serializer_class = ItemSerializer
    queryset = Item.objects.select_related('category').order_by('id')


class ItemDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemDetailSerializer
    lookup_field = "pk"


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        item_id = self.request.data.get('item_id')
        item = get_object_or_404(Item, id=item_id)
        existing_review = Review.objects.filter(
            item=item, created_by=self.request.user).exists()
        if existing_review:
            raise ValidationError("You have already reviewed this product.")

        serializer.save(created_by=self.request.user, item=item)
