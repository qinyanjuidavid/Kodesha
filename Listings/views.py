from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response


def PropertySubmissionView(request):
    return Response({"Message": "Submition endpoint"})


def PropertyListingView(request):
    return Response({"Message": "Property Listing"})
