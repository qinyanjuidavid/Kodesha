from django.urls import path
from Properties import views

app_name = "Properties"

urlpatterns = [
    path('submit/', views.PropertySubmissionView, name="propertySubmission"),
    path('listing/', views.PropertyListingView, name="propertyListing"),
]
