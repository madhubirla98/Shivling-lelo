from django.db import models

# Create your models here.

class CouponTypeChoices:

    PERCENTAGE = "PERCENTAGE"

    FIXED = "FIXED"

    CHOICES = (
        (PERCENTAGE, PERCENTAGE),
        (FIXED, FIXED),
    )

class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    coupon_type = models.CharField(
        max_length=20,
        choices=CouponTypeChoices.CHOICES
    )

    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    minimum_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    maximum_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    usage_limit = models.PositiveIntegerField(
        default=100
    )

    used_count = models.PositiveIntegerField(
        default=0
    )

    is_active = models.BooleanField(
        default=True
    )

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "coupons"

    def __str__(self):
        return self.code
