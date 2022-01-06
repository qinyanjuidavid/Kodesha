from Listings.serializers import PropertySerializer
from accounts.models import Administrator, User, Seller, Buyer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "full_name",
                  "email", "is_active", "phone",
                  "is_admin", "is_staff", "role", "timestamp")

        read_only_field = ("id", "is_active",
                           "is_admin", "is_staff", "role",
                           "timestamp")


class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Administrator
        fields = ("id", "user", "bio",
                  "profile_picture", "id_no", "town",
                  "estate", "timestamp")


class BuyerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Buyer
        fields = ("id", "user", "bio",
                  "profile_picture", "id_no", "town",
                  "estate", "timestamp")


class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Seller
        fields = ("id", "user", "bio",
                  "profile_picture", "id_no", "town",
                  "estate", "timestamp")


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=4, write_only=True, required=True)
    email = serializers.EmailField(
        required=True, max_length=128)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'phone', 'role', 'password']

    def create(self, validated_data):
        try:
            user = User.objects.get(email=validated_data['email'])
        except ObjectDoesNotExist:
            user = User.objects.create_user(**validated_data)
        return user


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=155, min_length=2
    )

    class Meta:
        fields = ['email', ]

    def validate(self, attrs):
        return attrs


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    password_confirmation = serializers.CharField(
        min_length=6, max_length=68, write_only=True
    )
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True
    )

    class Meta:
        fields = ("password", "password_confirmation", "token", "uidb64")

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password_confirmation = attrs.get('password_confirmation')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            if (password and password_confirmation
                    and password != password_confirmation):
                raise serializers.ValidationError(
                    {"Error": ("Passwords don\'t match!")}
                )
            if password == password_confirmation:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed(
                        "The Reset Link is Invalid!", 401
                    )
                user.set_password(password)
                user.save()
        except Exception as e:
            raise AuthenticationFailed("The Reset Link is Invalid!", 401)
        return super().validate(attrs)
