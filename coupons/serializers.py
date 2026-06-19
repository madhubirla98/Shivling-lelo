from rest_framework import serializers
from coupons.models import Coupon

class CouponValidationSerializer(
    serializers.Serializer
):

    coupon_code = serializers.CharField()

    order_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

class AdminCouponSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = Coupon
        fields = "__all__"