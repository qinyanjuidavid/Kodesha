from django.urls import path
from myapp import views
app_name='myapp'
urlpatterns=[
path('',views.home,name="home"),
path('house/<pk>/',views.house_details,name='details'),
path('dashboard/<pk>/',views.add_to_dashboard,name="add"),
path('dashboard/',views.myDashboard,name="dashboard"),
#path('like/',views.like_post,name="like")
]
