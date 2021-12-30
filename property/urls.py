from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('accounts.urls')),
    path('property/',include("Properties.urls"))
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
