from rest_framework import serializers

from carts.models import CartItem, Cart


class CartItemSerializer(
    serializers.ModelSerializer
):

    product_name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):

        return (
            obj.quantity
            * obj.product.price
        )

class CartSerializer(
    serializers.ModelSerializer
):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Cart

        fields = [
            "id",
            "user",
            "items",
            "grand_total",
        ]

    def get_grand_total(
        self,
        obj
    ):
        total = 0

        for item in obj.items.all():
            total += (
                item.product.price
                * item.quantity
            )

        return total