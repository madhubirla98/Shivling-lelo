from django.db.models import Sum
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product

from .models import CartItem
from .models import Cart
from .services import CartService
from .serializers import (
    CartSerializer
)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = (
            CartService
            .get_or_create_cart(
                request.user
            )
        )

        serializer = CartSerializer(
            cart
        )

        return Response(
            serializer.data
        )

class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        product_id = request.data.get(
            "product_id"
        )

        quantity = request.data.get(
            "quantity",
            1
        )

        product = Product.objects.get(
            id=product_id
        )

        CartService.add_product(
            request.user,
            product,
            quantity
        )

        return Response(
            {
                "message":
                "Product added to cart"
            },
            status=201
        )

class UpdateCartItemAPIView(
    APIView
):
    permission_classes = [IsAuthenticated]

    def put(
        self,
        request,
        item_id
    ):

        quantity = request.data.get(
            "quantity"
        )

        item = (
            CartItem.objects.get(
                id=item_id
            )
        )

        CartService.update_quantity(
            item,
            quantity
        )

        return Response(
            {
                "message":
                "Cart updated"
            }
        )


class RemoveCartItemAPIView(
    APIView
):
    permission_classes = [IsAuthenticated]
    def delete(
            self,
            request,
            item_id
    ):
        item = (
            CartItem.objects.get(
                id=item_id
            )
        )

        CartService.remove_item(
            item
        )

        return Response(
            status=204
        )

class CartCountAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        cart = (
            Cart.objects.filter(
                user=request.user
            ).first()
        )

        if not cart:
            return Response(
                {"count": 0}
            )

        count = (
            cart.items.aggregate(
                total=Sum(
                    "quantity"
                )
            )["total"]
            or 0
        )

        return Response(
            {"count": count}
        )
