from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from accounts.forms import RegistrationForm, UserUpdateForm,ProfileUpdateForm
from accounts.models import Profile
from django.contrib.auth.decorators import login_required


def register(request):
	if request.method=="POST":
		form=RegistrationForm(request.POST or None)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
	else:
		form=RegistrationForm()
	context={
	'form':form
	}
	return render(request,'accounts/register.html',context)

@login_required
def profiles(request):
	if request.method=="POST":
		user_form=UserUpdateForm(request.POST or None,request.FILES or None,instance=request.user)
		profile_form=ProfileUpdateForm(request.POST or None,request.FILES or None,instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			#messages.success(request,f'Your account has been updated!')
	else:
		user_form=UserUpdateForm()
		profile_form=ProfileUpdateForm()
	prof=Profile.objects.all()
	context={
	'prof':prof,
	'user_form':user_form,
	'profile_form':profile_form
	}
	return render(request,'accounts/profile.html',context)
