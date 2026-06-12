from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Address
from .selectors import get_user_addresses
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer, UpdateProfileSerializer, \
    ChangePasswordSerializer, AddressSerializer, AddressCreateSerializer
from .services import UserService, AddressService


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response({
                "message": "User created successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phone_number": user.phone_number
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        try:
            UserService.change_password(
                user=request.user,
                old_password=serializer.validated_data["old_password"],
                new_password=serializer.validated_data["new_password"],
            )

            return Response(
                {"message": "Password changed successfully"},
                status=status.HTTP_200_OK,
            )

        except ValidationError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class AddressListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = get_user_addresses(request.user)

        serializer = AddressSerializer(
            addresses,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AddressCreateSerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        address = AddressService.create_address(
            request.user,
            serializer.validated_data,
        )

        return Response(
            AddressSerializer(address).data,
            status=status.HTTP_201_CREATED,
        )

class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, address_id):
        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user,
        )

        serializer = AddressCreateSerializer(
            address,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        address = AddressService.update_address(
            address,
            serializer.validated_data,
        )

        return Response(
            AddressSerializer(address).data
        )

    def delete(self, request, address_id):
        address = get_object_or_404(
            Address,
            id=address_id,
            user=request.user,
        )

        AddressService.delete_address(address)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )