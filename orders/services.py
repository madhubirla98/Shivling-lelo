from django.db import transaction

from carts.models import Cart
from orders.models import (
    Order,
    OrderItem,
    OrderStatusChoices,
)
from products.models import (
    Inventory,
)

class OrderService:

    @staticmethod
    @transaction.atomic
    def checkout(user):

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

        total_amount = 0

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
                    "Insufficient stock"
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

            inventory.save()

            total_amount += (
                cart_item.product.price
                * cart_item.quantity
            )

        order.total_amount = total_amount
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