from django.urls import path
from accounts import views
from accounts.views import BuyerSignupView,SellerSignupView
from django.contrib.auth import views as auth_view
app_name='accounts'

urlpatterns=[
path('',auth_view.LoginView.as_view(template_name="accounts/login.html"),name='login'),
path('logout/',auth_view.LogoutView.as_view(template_name='accounts/logout.html'),name="logout"),
path('client/signup/',BuyerSignupView.as_view(),name="clientSignup"),
path('seller/signup/',SellerSignupView.as_view(),name="sellerSignup"),
# Password Reset
path('password_reset/',
         auth_view.PasswordResetView.as_view(
             template_name="passwords/password_reset.html",
             success_url='/password_reset/done/',
             email_template_name="passwords/password_reset_email.html",
             subject_template_name="passwords/password_reset_subject.txt"),
         name="password_reset"),
path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(
        template_name="passwords/password_reset_done.html",),
        name="password_reset_done"),
path('reset/<uidb64>/<token>/',
         auth_view.PasswordResetConfirmView.as_view(
             template_name="passwords/password_reset_confirm.html",
             success_url='/reset/done/'
         ),
         name="password_reset_confirm"
         ),
path('reset/done/', auth_view.PasswordResetCompleteView.as_view(
        template_name="passwords/password_reset_complete.html"),
        name="password_reset_complete"),
]
