from django.db import transaction
from decimal import Decimal

from carts.models import Cart
from orders.models import (
    Order,
    OrderItem,
    OrderStatusChoices,
)
from products.models import (
    Inventory,
)
from coupons.services import CouponService

class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user,
                 coupon_code=None
                 ):

        cart = Cart.objects.prefetch_related(
            "items__product"
        ).get(
            user=user
        )

        if not cart.items.exists():
            raise ValueError(
                "Cart is empty."
            )

        order = Order.objects.create(
            user=user
        )

        total_amount = Decimal("0.00")

        for cart_item in cart.items.all():

            inventory = (
                Inventory.objects
                .select_for_update()
                .get(
                    product=cart_item.product
                )
            )

            available_stock = (
                    inventory.quantity
                    - inventory.reserved_quantity
            )

            if (
                    cart_item.quantity
                    > available_stock
            ):
                raise ValueError(
                    f"Insufficient stock for "
                    f"{cart_item.product.name}"
                )

            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
            )

            inventory.quantity -= (
                cart_item.quantity
            )

            inventory.save(
                update_fields=[
                    "quantity"
                ]
            )

            total_amount += (
                    cart_item.product.price
                    * cart_item.quantity
            )

        discount_amount = Decimal("0.00")
        final_amount = total_amount
        coupon = None

        if coupon_code:
            coupon_result = (
                CouponService.validate_coupon(
                    coupon_code=coupon_code,
                    order_amount=total_amount,
                )
            )

            coupon = (
                coupon_result["coupon"]
            )

            discount_amount = (
                coupon_result["discount"]
            )

            final_amount = (
                coupon_result["final_amount"]
            )

            CouponService.mark_coupon_used(
                coupon
            )

        order.total_amount = total_amount
        order.discount_amount = (
            discount_amount
        )
        order.final_amount = (
            final_amount
        )
        order.coupon = coupon

        order.save()

        cart.items.all().delete()

        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(
            order
    ):

        if order.status not in [
            OrderStatusChoices.PENDING,
            OrderStatusChoices.PAID,
        ]:
            raise ValueError(
                "Order cannot be cancelled."
            )

        order.status = (
            OrderStatusChoices.CANCELLED
        )

        order.save()
        for item in order.items.all():
            inventory = (
                Inventory.objects.get(
                    product=item.product
                )
            )

            inventory.quantity += (
                item.quantity
            )

            inventory.save()
