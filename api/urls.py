from rest_framework.routers import SimpleRouter
from django.urls import path
from django.contrib.auth import views as auth_view
from accounts.views import (
    UserViewAPI,
)
routes = SimpleRouter()
app_name = 'accounts'
# Accounts
# routes.register('user/', UserViewAPI, basename='user')
urlpatterns = [
    path('users/', UserViewAPI, name="users")
]
