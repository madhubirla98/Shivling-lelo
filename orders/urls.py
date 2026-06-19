from django.urls import path

from .views import (
    CheckoutAPIView,OrderListView,OrderDetailView,CancelOrderAPIView
)
from django.urls import path

from .views import (
    AdminOrderListAPIView,
    AdminUpdateOrderStatusAPIView,
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
    path(
            "admin/orders/",
            AdminOrderListAPIView.as_view(),
            name="admin-order-list",
        ),

        path(
            "admin/orders/<int:order_id>/status/",
            AdminUpdateOrderStatusAPIView.as_view(),
            name="admin-update-order-status",
        ),

]