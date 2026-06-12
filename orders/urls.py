from django.urls import path

from .views import (
    CheckoutAPIView,OrderListView,OrderDetailView,CancelOrderAPIView
)

urlpatterns = [

    path(
        "",
        OrderListView.as_view()
    ),

    path(
        "<int:pk>/",
        OrderDetailView.as_view()
    ),

    path(
        "<int:order_id>/cancel/",
        CancelOrderAPIView.as_view()
    ),

    path(
        "checkout/",
        CheckoutAPIView.as_view()
    ),
]