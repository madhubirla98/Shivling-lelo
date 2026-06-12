from carts.models import Cart, CartItem
from products.models import Inventory


class CartService:

    @staticmethod
    def get_or_create_cart(user):

        cart, _ = (
            Cart.objects.get_or_create(
                user=user
            )
        )

        return cart

    @staticmethod
    def add_product(
        user,
        product,
        quantity
    ):
        inventory = Inventory.objects.get(
            product=product
        )

        available_stock = (
                inventory.quantity
                - inventory.reserved_quantity
        )

        if quantity > available_stock:
            raise ValueError(
                "Insufficient stock."
            )

        cart = (
            CartService
            .get_or_create_cart(user)
        )

        cart_item, created = (
            CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    "quantity": quantity
                }
            )
        )
        current_quantity = (
            cart_item.quantity
            if not created
            else 0
        )

        if (
                current_quantity
                + quantity
                >
                available_stock
        ):
            raise ValueError(
                "Insufficient stock."
            )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return cart_item

    @staticmethod
    def update_quantity(
        cart_item,
        quantity
    ):

        cart_item.quantity = quantity
        cart_item.save()

        return cart_item

    @staticmethod
    def remove_item(cart_item):

        cart_item.delete()