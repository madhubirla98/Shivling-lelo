from decimal import Decimal

from django.utils import timezone

from .models import (
Coupon,
CouponTypeChoices,
)

class CouponService:

    @staticmethod
    def validate_coupon(
        coupon_code,
        order_amount,
    ):
        """
        Validate coupon and calculate discount.
        """

        coupon = Coupon.objects.filter(
            code=coupon_code,
            is_active=True,
        ).first()

        if coupon is None:
            raise ValueError(
                "Invalid coupon."
            )

        current_time = timezone.now()

        if current_time < coupon.valid_from:
            raise ValueError(
                "Coupon is not active yet."
            )

        if current_time > coupon.valid_to:
            raise ValueError(
                "Coupon has expired."
            )

        if (
            coupon.used_count
            >= coupon.usage_limit
        ):
            raise ValueError(
                "Coupon usage limit exceeded."
            )

        order_amount = Decimal(
            str(order_amount)
        )

        if (
            order_amount
            < coupon.minimum_order_amount
        ):
            raise ValueError(
                f"Minimum order amount should be "
                f"{coupon.minimum_order_amount}"
            )

        discount = Decimal("0.00")

        if (
            coupon.coupon_type
            ==
            CouponTypeChoices.PERCENTAGE
        ):

            discount = (
                order_amount
                * coupon.discount_value
            ) / Decimal("100")

            if (
                coupon.maximum_discount
                and discount
                > coupon.maximum_discount
            ):
                discount = (
                    coupon.maximum_discount
                )

        elif (
            coupon.coupon_type
            ==
            CouponTypeChoices.FIXED
        ):

            discount = (
                coupon.discount_value
            )

            if discount > order_amount:
                discount = order_amount

        final_amount = (
            order_amount
            - discount
        )

        return {
            "coupon": coupon,
            "discount": discount,
            "final_amount": final_amount,
        }

    @staticmethod
    def mark_coupon_used(
        coupon,
    ):
        """
        Increment coupon usage count
        after successful checkout.
        """
    
        coupon.used_count += 1

        coupon.save(
            update_fields=[
                "used_count",
            ]
        )
