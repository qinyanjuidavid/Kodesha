from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from Properties.forms import PropertySubmissionForm
from Properties.models import Property


def PropertySubmissionView(request):
    form = PropertySubmissionForm()
    context = {
        "form": form
    }
    return render(request, "Properties/propertySubmission.html", context)


def PropertyListingView(request):
    propertyQs = Property.objects.filter(sold=False)
    context = {
        "properties": propertyQs
    }
    return render(request, "Properties/propertyListing.html", context)
