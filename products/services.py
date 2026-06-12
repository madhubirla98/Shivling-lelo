from rest_framework import generics

from .models import Category, Product, Inventory, ProductImage
from .serializers import ProductImageUploadSerializer


class CategoryService:

    @staticmethod
    def create_category(validated_data):
        return Category.objects.create(**validated_data)

    @staticmethod
    def update_category(category, validated_data):

        for field, value in validated_data.items():
            setattr(category, field, value)

        category.save()

        return category

class ProductService:

    @staticmethod
    def create_product(validated_data):

        return Product.objects.create(
            **validated_data
        )

    @staticmethod
    def update_product(
        product,
        validated_data
    ):
        for field, value in validated_data.items():
            setattr(
                product,
                field,
                value
            )

        product.save()

        return product

class InventoryService:

    @staticmethod
    def create_inventory(validated_data):

        return Inventory.objects.create(
            **validated_data
        )

    @staticmethod
    def update_inventory(
        inventory,
        validated_data
    ):

        for field, value in validated_data.items():
            setattr(
                inventory,
                field,
                value
            )

        inventory.save()

        return inventory

class ProductImageUploadView(
    generics.CreateAPIView
):

    serializer_class = ProductImageUploadSerializer

    def perform_create(self, serializer):

        product = Product.objects.get(
            id=self.kwargs["product_id"]
        )
        # if serializer.validated_data.get(
        #         "is_primary"
        # ):
        #     ProductImage.objects.filter(
        #         product=product,
        #         is_primary=True
        #     ).update(
        #         is_primary=False
        #     )

        serializer.save(
            product=product
        )