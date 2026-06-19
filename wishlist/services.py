from .models import Wishlist


class WishlistService:

    @staticmethod
    def add_product(
        user,
        product
    ):
        Wishlist.objects.get_or_create(
            user=user,
            product=product
        )

    @staticmethod
    def remove_product(
        user,
        product
    ):
        Wishlist.objects.filter(
            user=user,
            product=product
        ).delete()