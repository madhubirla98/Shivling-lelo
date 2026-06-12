from django.urls import path

from .services import ProductImageUploadView
from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView, ProductListCreateAPIView, ProductDetailAPIView, InventoryListCreateAPIView,
    InventoryDetailAPIView, ProductImageListAPIView, ProductImageDeleteAPIView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateAPIView.as_view(),
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailAPIView.as_view(),
    ),
path(
    "products/",
    ProductListCreateAPIView.as_view(),
),

path(
    "products/<int:pk>/",
    ProductDetailAPIView.as_view(),
),
path(
    "inventories/",
    InventoryListCreateAPIView.as_view(),
),

path(
    "inventories/<int:pk>/",
    InventoryDetailAPIView.as_view(),
),
path(
    "<int:product_id>/images/",
    ProductImageUploadView.as_view(),
    name="product-image-upload"
),
path(
    "products/<int:product_id>/images/list/",
    ProductImageListAPIView.as_view()
),

path(
    "images/<int:image_id>/",
    ProductImageDeleteAPIView.as_view()
),
]