from django.urls import path
from .views import RegisterView, LoginView, ProfileView, ChangePasswordView, AddressListCreateView, AddressDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view()),
    path("addresses/", AddressListCreateView.as_view()),
    path("addresses/<int:address_id>/",AddressDetailView.as_view()),
]