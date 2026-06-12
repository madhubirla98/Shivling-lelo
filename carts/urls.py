from django.urls import path

from .views import (
    CartAPIView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    RemoveCartItemAPIView,
)

urlpatterns = [

    path(
        "",
        CartAPIView.as_view()
    ),

    path(
        "add/",
        AddToCartAPIView.as_view()
    ),

    path(
        "items/<int:item_id>/",
        UpdateCartItemAPIView.as_view()
    ),

    path(
        "items/<int:item_id>/delete/",
        RemoveCartItemAPIView.as_view()
    ),
]