from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from Listings.serializers import PropertySerializer, PropertyTypeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User
from Listings.models import Property, Property_Type


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


@api_view(["GET", ])
@permission_classes([AllowAny])
def PropertyListingView(request):
    propertyQuery = Property.objects.filter(
        sold=False, rented=False,
        list=True).order_by("-featured")
    if request.method == "GET":
        serializer = PropertySerializer(propertyQuery, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)
