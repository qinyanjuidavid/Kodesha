from rest_framework.routers import SimpleRouter
from django.urls import path
from django.contrib.auth import views as auth_view
from accounts.views import (
    UserViewAPI,
    LoginViewSet,
    RegistrationViewSet,
    RefreshViewSet
)
from Listings.views import (
    PropertySubmissionView,
    PropertyListingView,
)
routes = SimpleRouter()
app_name = 'accounts'
# Accounts
routes.register(r'login', LoginViewSet, basename='login')
routes.register(r'register', RegistrationViewSet, basename='register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register("property/submission", PropertySubmissionView,
                basename="propertySubmission")
urlpatterns = [
    *routes.urls,
    path('users/', UserViewAPI, name="users"),
    path('property/listings/',
         PropertyListingView, name="propertyListing"),
]
