from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Category, Product, Inventory, ProductImage
from .pagination import ProductPagination
from .serializers import CategorySerializer, ProductSerializer, InventorySerializer, ProductImageSerializer
from .services import CategoryService, ProductService, InventoryService
from .selectors import CategorySelector, ProductSelector, InventorySelector


class CategoryListCreateAPIView(APIView):

    def get(self, request):

        categories = CategorySelector.get_categories()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = CategorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.create_category(
            serializer.validated_data
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )

class CategoryDetailAPIView(APIView):

    def get_object(self, pk):
        return Category.objects.get(pk=pk)

    def get(self, request, pk):

        category = self.get_object(pk)

        serializer = CategorySerializer(category)

        return Response(serializer.data)

    def put(self, request, pk):

        category = self.get_object(pk)

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        category = CategoryService.update_category(
            category,
            serializer.validated_data
        )

        return Response(
            CategorySerializer(category).data
        )

    def delete(self, request, pk):

        category = self.get_object(pk)

        category.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class ProductListCreateAPIView(APIView):

    def get(self, request):
        filters = {
            "search": request.GET.get(
                "search"
            ),
            "category": request.GET.get(
                "category"
            ),
            "min_price": request.GET.get(
                "min_price"
            ),
            "max_price": request.GET.get(
                "max_price"
            ),
        }

        products = (
            ProductSelector
            .get_products(filters)
        )

        paginator = ProductPagination()

        paginated_products = (
            paginator.paginate_queryset(
                products,
                request
            )
        )

        serializer = (
            ProductSerializer(
                paginated_products,
                many=True
            )
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self, request):

        serializer = ProductSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        product = (
            ProductService
            .create_product(
                serializer.validated_data
            )
        )

        return Response(
            ProductSerializer(
                product
            ).data,
            status=status.HTTP_201_CREATED
        )

class ProductDetailAPIView(APIView):

    def get_object(self, pk):

        return Product.objects.get(
            pk=pk
        )

    def get(self, request, pk):

        product = self.get_object(pk)

        serializer = ProductSerializer(
            product
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):

        product = self.get_object(pk)

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        product = (
            ProductService
            .update_product(
                product,
                serializer.validated_data
            )
        )

        return Response(
            ProductSerializer(
                product
            ).data
        )

    def delete(self, request, pk):

        product = self.get_object(pk)

        product.is_active = False
        product.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class InventoryListCreateAPIView(APIView):

    def get(self, request):

        inventories = (
            InventorySelector
            .get_inventories()
        )

        serializer = InventorySerializer(
            inventories,
            many=True
        )

        return Response(
            serializer.data
        )

    def post(self, request):

        serializer = InventorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        inventory = (
            InventoryService
            .create_inventory(
                serializer.validated_data
            )
        )

        return Response(
            InventorySerializer(
                inventory
            ).data,
            status=status.HTTP_201_CREATED
        )

class InventoryDetailAPIView(APIView):

    def get_object(self, pk):

        return Inventory.objects.get(
            pk=pk
        )

    def get(self, request, pk):

        inventory = self.get_object(pk)

        serializer = InventorySerializer(
            inventory
        )

        return Response(
            serializer.data
        )

    def put(self, request, pk):

        inventory = self.get_object(pk)

        serializer = InventorySerializer(
            inventory,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        inventory = (
            InventoryService
            .update_inventory(
                inventory,
                serializer.validated_data
            )
        )

        return Response(
            InventorySerializer(
                inventory
            ).data
        )

    def delete(self, request, pk):

        inventory = self.get_object(pk)

        inventory.delete()

        return Response(status=204)


class ProductImageListAPIView(
    APIView
):

    def get(
        self,
        request,
        product_id
    ):

        product = (
            get_object_or_404(
                Product,
                id=product_id
            )
        )

        images = (
            product.images.all()
        )

        serializer = (
            ProductImageSerializer(
                images,
                many=True,
                context={
                    "request": request
                }
            )
        )

        return Response(
            serializer.data
        )

class ProductImageDeleteAPIView(
    APIView
):

    def delete(
        self,
        request,
        image_id
    ):

        image = (
            get_object_or_404(
                ProductImage,
                id=image_id
            )
        )

        image.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )