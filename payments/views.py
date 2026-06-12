from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import (
    Response
)

from orders.models import Order

from .services import (
    PaymentService
)

from .serializers import (
    PaymentSerializer
)
from django.db import transaction

from .models import (
    Payment,
    PaymentStatusChoices
)

from orders.models import (
    OrderStatusChoices
)

class CreatePaymentAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        order = Order.objects.get(
            id=request.data["order_id"],
            user=request.user
        )

        payment = (
            PaymentService.create_payment(
                order
            )
        )

        return Response(
            PaymentSerializer(
                payment
            ).data
        )

class PaymentSuccessAPIView(
    APIView
):

    @transaction.atomic
    def post(
        self,
        request,
        payment_id
    ):

        payment = Payment.objects.select_for_update().get(
            id=payment_id
        )

        payment.status = (
            PaymentStatusChoices.SUCCESS
        )

        payment.transaction_id = (
            "TXN123456"
        )

        payment.save()

        payment.order.status = (
            OrderStatusChoices.PAID
        )

        payment.order.save()

        return Response(
            {
                "message":
                "Payment Success"
            }
        )