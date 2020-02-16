from django.contrib import admin
from myapp.models import House,Interesting_house,Dashboard

class HouseAdmin(admin.ModelAdmin):
    pass
admin.site.register(House,HouseAdmin)
admin.site.register(Interesting_house)
admin.site.register(Dashboard)
