from rest_framework.routers import SimpleRouter
from django.urls import path
from django.contrib.auth import views as auth_view
from accounts.views import (
    LoginViewSet,
    RegistrationViewSet,
    RefreshViewSet, SetNewPasswordAPIView,
    VerifyEmail, PasswordTokenCheckAPI,
    RequestPasswordResetEmail, AdminProfileAPIView,
    SellerProfileAPIView, BuyerProfileAPIView
)
from Listings.views import (
    PropertySubmissionView,
    PropertyListingView,
    propertyDetailsView,
    SellerPropertyListView,
    SellerPropertyUpdateView,
)
routes = SimpleRouter()
app_name = 'api'
# Accounts
routes.register(r'login', LoginViewSet, basename='login')
routes.register(r'register', RegistrationViewSet, basename='register')
routes.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')
routes.register("property/submission", PropertySubmissionView,
                basename="propertySubmission")
routes.register("myproperty/details", SellerPropertyUpdateView,
                basename="propertyUpdate")
routes.register('myproperty', SellerPropertyListView,
                basename="sellerProperty")
routes.register('password-reset', RequestPasswordResetEmail,
                basename="requestPasswordReset")
routes.register('password-reset-complete',  SetNewPasswordAPIView,
                basename="password-reset-complete")

routes.register('admin/profile', AdminProfileAPIView,
                basename="adminProfile")
routes.register('seller/profile', SellerProfileAPIView,
                basename="sellerProfile")
routes.register('buyer/profile', BuyerProfileAPIView,
                basename="buyerProfile")
urlpatterns = [
    *routes.urls,
    path('property/listings/',
         PropertyListingView, name="propertyListing"),
    path('property/<int:id>/details/',
         propertyDetailsView, name="propertyDetails"),
    path('activate/', VerifyEmail.as_view(),
         name="email-verify"),
    path('password-reset/', RequestPasswordResetEmail,
         name="password-reset"),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(),
         name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView,
         name="password-reset-complete"),
]
