from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import transaction

from users.models import Address

User = get_user_model()


class UserService:

    @staticmethod
    def create_user(validated_data):
        password = validated_data.pop("password")

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

    @staticmethod
    def change_password(user, old_password, new_password):
        if not user.check_password(old_password):
            raise ValidationError("Old password is incorrect")

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return user

class AddressService:

    @staticmethod
    @transaction.atomic
    def create_address(user, validated_data):

        is_default = validated_data.get(
            "is_default",
            False
        )

        if is_default:
            Address.objects.filter(
                user=user,
                is_default=True
            ).update(is_default=False)

        return Address.objects.create(
            user=user,
            **validated_data
        )

    @staticmethod
    def update_address(address, validated_data):
        for field, value in validated_data.items():
            setattr(address, field, value)

        address.save()
        return address

    @staticmethod
    def delete_address(address):
        address.delete()