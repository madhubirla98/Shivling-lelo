from django.contrib.auth.models import AbstractUser
from django.db import models

class UserRoleChoices:

    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"

    CHOICES = (
        (CUSTOMER, CUSTOMER),
        (ADMIN, ADMIN),
    )

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.CHOICES,
        default=UserRoleChoices.CUSTOMER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

from django.conf import settings
from django.db import models


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )

    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "addresses"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.city}"
