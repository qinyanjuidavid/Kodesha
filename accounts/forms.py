from accounts.models import User,Administrator,Seller,Buyer
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.db import transaction

class UserSignupForm(forms.ModelForm):
    email=forms.EmailField(max_length=156,required=True)
    phone=forms.CharField(max_length=20,required=True)

    class Meta:
        model=User
        fields=('username','phone','email','role')

    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Password Confirmation",widget=forms.PasswordInput)

    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")

        if password1 and password2 and password1 !=password2:
            raise forms.ValidationError("Password don\'t match!")

        return password2

    @transaction.atomic
    def save(self,commit=True):
        user=super().save(commit=False)
        user.is_active=False
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
