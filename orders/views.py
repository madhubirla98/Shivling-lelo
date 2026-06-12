from django.shortcuts import render

# Create your views here.
from rest_framework.views import (
    APIView
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import (
    Response
)

from .services import (
    OrderService
)

from .serializers import (
    OrderSerializer
)

class CheckoutAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        order = (
            OrderService.checkout(
                request.user
            )
        )

        return Response(
            OrderSerializer(
                order
            ).data,
            status=201
        )

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)

from .models import Order
from .serializers import (
    OrderSerializer
)


class OrderListView(
    generics.ListAPIView
):

    serializer_class = (
        OrderSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            Order.objects
            .filter(
                user=self.request.user
            )
            .prefetch_related(
                "items"
            )
            .order_by(
                "-created_at"
            )
        )

class OrderDetailView(
    generics.RetrieveAPIView
):

    serializer_class = (
        OrderSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return (
            Order.objects
            .filter(
                user=self.request.user
            )
            .prefetch_related(
                "items"
            )
        )

class CancelOrderAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request,
        order_id
    ):

        order = (
            Order.objects.get(
                id=order_id,
                user=request.user
            )
        )

        OrderService.cancel_order(
            order
        )

        return Response(
            {
                "message":
                "Order cancelled"
            }
        )