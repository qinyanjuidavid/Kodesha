from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from myapp.models import House,Interesting_house,Dashboard
from django.utils import timezone



def home(request):
    house_obj=House.objects.all()
    context={
    'house_obj':house_obj
    }
    return render(request,'myapp/home.html',context)

def house_details(request,pk):
    details_obj=House.objects.get(pk=pk)
    context={
    'details_obj':details_obj
    }
    return render(request,'myapp/details.html',context)
def add_to_dashboard(request,pk):
    house=House.objects.get(pk=pk)
    interesting,created=Interesting_house.objects.get_or_create(house=house,user=request.user)
    dash=Dashboard.objects.filter(user=request.user)
    if dash.exists():
        dash=dash[0]
        if dash.houses.filter(house__pk=house.pk).exists():
            interesting.save()
        else:
            dash.houses.add(interesting)
    else:
        date_added=timezone.now()
        dash=Dashboard.objects.create(user=request.user,date_added=date_added)
        dash.houses.add(interesting)
    return HttpResponseRedirect(f'/myapp/house/{pk}/')
def myDashboard(request):
    dash=Dashboard.objects.all().order_by('-date_added')
    context={
    'dash':dash,
    }
    return render(request,'myapp/dashboard.html',context)
