from django.db import models

# Create your models here.
from django.conf import settings
from django.db import models

from products.models import Product


class Wishlist(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "wishlist"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_product_wishlist"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.product.name}"
        )
