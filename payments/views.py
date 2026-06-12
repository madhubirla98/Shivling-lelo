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
