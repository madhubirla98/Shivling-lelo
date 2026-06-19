from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from products.models import Product

from .services import WishlistService
from rest_framework import generics

from .models import Wishlist
from .serializers import (
    WishlistSerializer
)

class AddToWishlistAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        product = Product.objects.get(
            id=request.data["product_id"]
        )

        WishlistService.add_product(
            request.user,
            product
        )

        return Response(
            {
                "message":
                "Added to wishlist"
            }
        )

class WishlistListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        WishlistSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            Wishlist.objects
            .filter(
                user=self.request.user
            )
            .select_related(
                "product"
            )
            .order_by(
                "-created_at"
            )
        )

class RemoveWishlistAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(
        self,
        request,
        product_id
    ):

        product = Product.objects.get(
            id=product_id
        )

        WishlistService.remove_product(
            request.user,
            product
        )

        return Response(
            {
                "message":
                "Removed from wishlist"
            }
        )