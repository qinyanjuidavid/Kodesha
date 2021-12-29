from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.base import File
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView
from accounts.tokens import account_activation_token
from accounts.sendMails import send_activation_mail
from accounts.models import User
from accounts.forms import UserSignupForm

class BuyerSignupView(CreateView):
	model=User
	form_class=UserSignupForm
	template_name="accounts/clientSignup.html"

	def get_context_data(self,**kwargs):
		kwargs['user_type'] = 'client'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		if form.is_valid():
			user = form.save(commit=False)
			user.role = "Role"
			user.save()
			send_activation_mail(user, self.request)
		return render(self.request, "accounts/sign_alert.html")

class SellerSignupView(CreateView):
	model=User
	form_class=UserSignupForm
	template_name="accounts/sellerSignup.html"

	def get_context_data(self,**kwargs):
		kwargs['user_type'] = 'client'
		return super().get_context_data(**kwargs)

	def form_valid(self, form):
		if form.is_valid():
			user = form.save(commit=False)
			user.role="Seller"
			user.save()
			send_activation_mail(user, self.request)
		return render(self.request, "accounts/sign_alert.html")



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)

        return render(request, 'accounts/activate_success.html')
    else:
        return render(request, 'accounts/activate_fail.html')
