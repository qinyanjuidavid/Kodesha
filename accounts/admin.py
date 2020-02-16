from django.contrib import admin
from accounts.models import User, Profile
from accounts.forms import UserChangeForm,UserCreationForm

class useradmin(admin.ModelAdmin):
    search_fields=['email']
    form=UserChangeForm
    add_form=UserCreationForm
    list_display=('username','email','admin','staff','active','timestamp')
    list_filter=('admin','staff','active')


admin.site.register(User,useradmin)
admin.site.register(Profile)
