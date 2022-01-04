from django.db.models import query
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets
from Listings.serializers import PropertySerializer, PropertyTypeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User, Seller
from Listings.models import Property, Property_Type


class PropertySubmissionView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = ()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        userObj = Seller.objects.get(id=1)
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


@api_view(["GET", ])
@permission_classes([AllowAny])
def propertyDetailsView(request, id):
    propertyQs = Property.objects.get(
        id=id, sold=False, rented=False, list=True)
    if request.method == "GET":
        serializer = PropertySerializer(propertyQs, many=False)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

# Individuals properties
# Sellers can see their properties


class SellerPropertyListView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = ()
    http_method_names = ['get', ]
    sellerQuery = Seller.objects.get(id=1)
    queryset = Property.objects.filter(added_by=sellerQuery)

    def list(self, request):
        serializer = self.get_serializer(
            self.queryset, many=True
        )
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class SellerPropertyUpdateView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = ()
    http_method_names = ["get", "put", "delete"]
    ownerQuery = Seller.objects.get(id=1)
    queryset = Property.objects.filter(added_by=ownerQuery)

    def retrieve(self, request, pk=None, *args, **kwargs):
        property = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(
            property)

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        property = get_object_or_404(self.queryset, pk=pk)
        serializer = self.get_serializer(
            instance=property, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk=None, *args, **kwargs):
        property = get_object_or_404(self.queryset, pk=pk)
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
