from rest_framework import serializers

from .models import Category, Product, Inventory, ProductImage


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class ProductImageSerializer(
    serializers.ModelSerializer
):

    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image_url",
            "is_primary",
        )

    def get_image_url(self, obj):

        request = self.context.get(
            "request"
        )

        if request:
            return request.build_absolute_uri(
                obj.image.url
            )

        return obj.image.url



class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "images",
        )

    def validate_category(self, value):

        if not Category.objects.filter(
            id=value.id
        ).exists():
            raise serializers.ValidationError(
                "Invalid category."
            )

        return value

class InventorySerializer(serializers.ModelSerializer):

    available_quantity = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = "__all__"

class ProductImageUploadSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "is_primary",
        )

