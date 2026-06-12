from django.db import models
from orders.models import Order
# Create your models here.
class PaymentStatusChoices:

    CREATED = "CREATED"

    PENDING = "PENDING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    REFUNDED = "REFUNDED"

    CHOICES = (
        (CREATED, CREATED),
        (PENDING, PENDING),
        (SUCCESS, SUCCESS),
        (FAILED, FAILED),
        (REFUNDED, REFUNDED),
    )

class Payment(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        related_name="payments"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatusChoices.CHOICES,
        default=PaymentStatusChoices.CREATED
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "payments"
