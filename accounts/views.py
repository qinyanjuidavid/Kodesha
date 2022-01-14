import jwt
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import File
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.db.models import Q, query
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_str, force_text, smart_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.models import Administrator, Buyer, Seller, User
from accounts.sendMails import send_activation_mail, send_password_reset_email
from accounts.serializers import (AdminProfileSerializer,
                                  BuyerProfileSerializer, LoginSerializer,
                                  RegisterSerializer,
                                  ResetPasswordEmailRequestSerializer,
                                  SellerProfileSerializer,
                                  SetNewPasswordSerializer, UserSerializer)
from accounts.tokens import account_activation_token


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        user_data = serializer.data
        send_activation_mail(user_data, request)

        refresh = RefreshToken.for_user(user)
        res = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response({
            "user": serializer.data,
            "refresh": res['refresh'],
                        "token": res['access']
                        }, status=status.HTTP_201_CREATED)


class RefreshViewSet(viewsets.ViewSet, TokenRefreshView):
    permission_classes = (AllowAny,)
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms="HS256"
            )
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response(
                {"Email": "Account was Successully Verified"},
                status=status.HTTP_200_OK
            )
        except jwt.ExpiredSignatureError as identifier:
            return Response({
                "Error": "The Action Link Expired!"
            },
                status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecoderError as identifier:
            raise Response({
                "Error": "Invalid Activation Link!"
            },
                status=status.HTTP_400_BAD_REQUEST
            )
# Password Reset


class RequestPasswordResetEmail(ModelViewSet):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post", ]

    def create(self, request, *args, **kwargs):
        self.get_serializer(data=request.data)
        email = request.data["email"]
        if User.objects.filter(email=email):
            user = User.objects.get(email=email)
            if user.is_active:
                send_password_reset_email(user, request)
            return Response(
                {"Success": "We have emailed you a link to reset your password"},
                status=status.HTTP_200_OK
            )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "Error":
                    "Token is no longer valid, Please request a new one."
                },
                    status=status.HTTP_401_UNAUTHORIZED
                )
            return Response({
                "Success": True,
                "message": "Password Reset Successful",
                "uidb64": uidb64,
                "token": token
            })
        except DjangoUnicodeDecodeError as identifier:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "Error":
                    "Token is no longer valid, Please request a new one."
                },
                    status=status.HTTP_401_UNAUTHORIZED
                )


class SetNewPasswordAPIView(ModelViewSet):
    serializer_class = SetNewPasswordSerializer
    permission_classes = ()
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class AdminProfileAPIView(ModelViewSet):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", ]

    def get_queryset(self):
        user = self.request.user
        adminQuery = Administrator.objects.filter(
            Q(user=user)
        )
        # X-CSRFToken
        return adminQuery

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        userSerializer = UserSerializer(
            request.user, data=request.data["user"])
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerProfileAPIView(ModelViewSet):
    serializer_class = SellerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put"]

    def get_queryset(self):
        user = self.request.user
        sellerQuery = Seller.objects.filter(
            Q(user=user)
        )
        return sellerQuery

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        userSerializer = UserSerializer(
            request.user, data=request.data["user"]
        )
        userSerializer.is_valid(raise_exception=True)
        userSerializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class BuyerProfileAPIView(ModelViewSet):
    serializer_class = BuyerProfileSerializer
    permission_classes = [IsAuthenticated]
    http_methods_names = ["get", "put"]

    def get_queryset(self):
        user = self.request.user
        buyerQuery = Buyer.objects.filter(
            Q(user=user)
        )
        return buyerQuery

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
