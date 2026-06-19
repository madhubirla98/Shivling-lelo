from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics

from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from .serializers import (
    CouponValidationSerializer, AdminCouponSerializer
)

from .services import (
    CouponService
)
from users.permissions import IsAdminUserRole
from coupons.models import Coupon

class ValidateCouponAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):

        serializer = (
            CouponValidationSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        result = (
            CouponService.validate_coupon(
                coupon_code=
                serializer.validated_data[
                    "coupon_code"
                ],
                order_amount=
                serializer.validated_data[
                    "order_amount"
                ]
            )
        )

        return Response(
            {
                "coupon":
                    result[
                        "coupon"
                    ].code,
                "discount":
                    result[
                        "discount"
                    ],
                "final_amount":
                    result[
                        "final_amount"
                    ],
            }
        )


class AdminCouponCreateAPIView(
    generics.CreateAPIView
):

    serializer_class = (
        AdminCouponSerializer
    )

    permission_classes = [
        IsAdminUserRole
    ]

class AdminCouponListAPIView(
    generics.ListAPIView
):

    serializer_class = (
        AdminCouponSerializer
    )

    permission_classes = [
        IsAdminUserRole
    ]

    queryset = (
        Coupon.objects.all()
        .order_by("-id")
    )

class AdminCouponUpdateAPIView(
    generics.UpdateAPIView
):

    serializer_class = (
        AdminCouponSerializer
    )

    permission_classes = [
        IsAdminUserRole
    ]

    queryset = Coupon.objects.all()


class AdminCouponDisableAPIView(
    APIView
):

    permission_classes = [
        IsAdminUserRole
    ]

    def patch(
        self,
        request,
        coupon_id
    ):

        coupon = Coupon.objects.get(
            id=coupon_id
        )

        coupon.is_active = False

        coupon.save(
            update_fields=[
                "is_active"
            ]
        )

        return Response(
            {
                "message":
                "Coupon disabled."
            }
        )