from accounts.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def send_activation_mail(user, request):
    current_site = get_current_site(request)
    mail_subject = "Please Activate Your Account."

    message = render_to_string("accounts/activate_email.html", {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
    })

    to_mail = user.email
    email = EmailMessage(mail_subject, message, to=[to_mail])

    email.send()
