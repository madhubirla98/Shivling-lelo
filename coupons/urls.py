from django.urls import path

from .views import (
    ValidateCouponAPIView,AdminCouponCreateAPIView,AdminCouponListAPIView,
    AdminCouponUpdateAPIView,AdminCouponDisableAPIView
)

urlpatterns = [

    path(
        "validate/",
        ValidateCouponAPIView.as_view()
    ),
path(
    "admin/coupons/",
    AdminCouponCreateAPIView.as_view(),
),

path(
    "admin/coupons/list/",
    AdminCouponListAPIView.as_view(),
),

path(
    "admin/coupons/<int:pk>/",
    AdminCouponUpdateAPIView.as_view(),
),

path(
    "admin/coupons/<int:coupon_id>/disable/",
    AdminCouponDisableAPIView.as_view(),
),
]