from .models import (
    Payment,
    PaymentStatusChoices
)

class PaymentService:

    @staticmethod
    def create_payment(order):

        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            status=PaymentStatusChoices.CREATED
        )

        return payment