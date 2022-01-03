from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from Listings.serializers import PropertySerializer, PropertyTypeSerializer

from accounts.models import User


class PropertySubmissionView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = ()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        userObj = User.objects.get(id=1)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by=userObj)
        return Response(serializer.data)


def PropertyListingView(request):

    return Response({"Message": "Property Listing"})
