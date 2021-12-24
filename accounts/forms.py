# from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from accounts.models import User, Profile
#
#
# class UserCreationForm(ModelForm):
#     class Meta:
#         model=User
#         fields=('email','username')
#
#     password1=forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2=forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
#
#     def clean_password(self):
#         password1=self.cleaned_data.get('password1')
#         password2=self.cleaned_data.get('password2')
#
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError('Passwords Dont match')
#
#     def save(self,commit=True):
#         user=super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#
#         return user
#
#
# class UserChangeForm(ModelForm):
#     password=ReadOnlyPasswordHashField
#     class Meta:
#         model=User
#         fields=('email','username','password','active','admin')
#
#     def clean_password(self):
#         return self.initial ['password']
#
#
# class RegistrationForm(ModelForm):
#         class Meta:
#             model=User
#             fields=('email','username')
#
#         password1=forms.CharField(label='Password', widget=forms.PasswordInput)
#         password2=forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
#
#         def clean_password(self):
#             password1=self.cleaned_data.get('password1')
#             password2=self.cleaned_data.get('password2')
#
#             if password1 and password2 and password1 != password2:
#                 raise forms.ValidationError('Passwords Dont match')
#
#         def save(self,commit=True):
#             user=super(RegistrationForm, self).save(commit=False)
#             user.set_password(self.cleaned_data["password1"])
#             if commit:
#                 user.save()
#
#             return user
#
# class UserUpdateForm(ModelForm):
#     class Meta:
#         model=User
#         fields=['username','email']
#
# class ProfileUpdateForm(ModelForm):
#     class Meta:
#         model=Profile
#         fields=['image']
