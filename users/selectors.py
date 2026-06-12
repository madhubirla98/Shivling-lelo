from users.models import Address


def get_user_addresses(user):
    return Address.objects.filter(
        user=user
    )

def get_user_address(user, address_id):
    return Address.objects.get(
        id=address_id,
        user=user
    )