from django.db.models import Q

from .models import Category, Product, Inventory


class CategorySelector:

    @staticmethod
    def get_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(category_id):
        return Category.objects.get(id=category_id)

class ProductSelector:

        @staticmethod
        def get_products(filters=None):

            queryset = (
                Product.objects
                .select_related("category")
                .all()
            )

            if not filters:
                return queryset

            search = filters.get("search")

            if search:
                queryset = queryset.filter(
                    Q(name__icontains=search)
                    |
                    Q(description__icontains=search)
                )

            category = filters.get("category")

            if category:
                queryset = queryset.filter(
                    category_id=category
                )

            min_price = filters.get("min_price")

            if min_price:
                queryset = queryset.filter(
                    price__gte=min_price
                )

            max_price = filters.get("max_price")

            if max_price:
                queryset = queryset.filter(
                    price__lte=max_price
                )

            return queryset

        @staticmethod
        def get_product(product_id):

            return Product.objects.select_related(
                "category"
            ).get(
                id=product_id
            )

class InventorySelector:

    @staticmethod
    def get_inventories():

        return Inventory.objects.select_related(
            "product"
        )

    @staticmethod
    def get_inventory(pk):

        return Inventory.objects.select_related(
            "product"
        ).get(
            pk=pk
        )