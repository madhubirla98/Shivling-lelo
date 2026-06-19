from django.urls import path
from .views import *

urlpatterns = [

    path(
        "",
        WishlistListAPIView.as_view()
    ),

    path(
        "add/",
        AddToWishlistAPIView.as_view()
    ),

    path(
        "remove/<int:product_id>/",
        RemoveWishlistAPIView.as_view()
    ),
]