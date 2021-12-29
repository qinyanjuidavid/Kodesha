from django.contrib import admin
from accounts.models import User, Buyer,Seller,Administrator

admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Seller)
admin.site.register(Buyer)
