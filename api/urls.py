from rest_framework.routers import SimpleRouter
from django.urls import path
from django.contrib.auth import views as auth_view
from accounts.views import (
    UserViewAPI,
    LoginViewSet,
    RegistrationViewSet
)
routes = SimpleRouter()
app_name = 'accounts'
# Accounts
routes.register('login/', LoginViewSet, basename='login')
routes.register('register/', RegistrationViewSet, basename='register')

urlpatterns = [
    *routes.urls,
    path('users/', UserViewAPI, name="users")
]
