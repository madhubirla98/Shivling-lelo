from django.shortcuts import render
from rest_framework import status

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
from rest_framework import generics
from .models import Order
from users.permissions import (
    IsAdminUserRole
)
from .serializers import (
    UpdateOrderStatusSerializer
)

# Customer APIs
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

        order = OrderService.checkout(
                  user=request.user,
                 coupon_code=request.data.get("coupon_code"))

        return Response(
            OrderSerializer(
                order
            ).data,
            status=201
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

# Admin API's
class AdminOrderListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        OrderSerializer
    )

    permission_classes = [
        IsAdminUserRole
    ]

    queryset = (
        Order.objects
        .all()
        .select_related(
            "user"
        )
        .prefetch_related(
            "items"
        )
        .order_by(
            "-created_at"
        )
    )

class AdminUpdateOrderStatusAPIView(
    APIView
):

    permission_classes = [
        IsAdminUserRole
    ]

    def patch(
        self,
        request,
        order_id
    ):

        serializer = (
            UpdateOrderStatusSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        order = Order.objects.get(
            id=order_id
        )

        order.status = (
            serializer.validated_data[
                "status"
            ]
        )
        valid_statuses = [
            "PENDING",
            "PAID",
            "PROCESSING",
            "SHIPPED",
            "DELIVERED",
            "CANCELLED",
        ]

        new_status = (
            serializer.validated_data[
                "status"
            ]
        )

        if new_status not in valid_statuses:
            raise ValueError(
                "Invalid order status."
            )

        order.save(
            update_fields=[
                "status"
            ]
        )

        return Response(
            {
                "message":
                "Order status updated.",
                "order_id":
                order.id,
                "status":
                order.status,
            },
            status=status.HTTP_200_OK
        )