from django.db.models import query, Q
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, viewsets
from Listings.serializers import (PropertySerializer,
                                  PropertyTypeSerializer)
from rest_framework.permissions import IsAuthenticated, AllowAny

from accounts.models import User, Seller
from Listings.models import (Property,
                             Property_Type)
from rest_framework.decorators import action
from rest_framework.parsers import (FormParser,
                                    MultiPartParser,
                                    JSONParser)


class PropertySubmissionView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["post", "get", "put", "delete"]
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get_queryset(self, request):
        return Property.objects.filter(
            Q(added_by__user=request.user)
        )

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = PropertySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = PropertySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(added_by__user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset(request)
        queryset = get_object_or_404(queryset, pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset(request)
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = PropertySerializer(queryset,
                                        data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

        # @action(detail=True, method=['put'])
        # def upload(self, request, pk=None, *args, **kwargs):
        #     pass
        # --> Image upload


class PropertyListingView(ModelViewSet):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny, ]
    http_method_names = ["get"]

    def get_queryset(self, request):
        return Property.objects.filter(
            Q(sold=False) |
            Q(rented=False) |
            Q(list=True)
        ).order_by("-featured")

    def list(self, request):
        queryset = self.get_queryset(request)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset(request)
        queryset = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(queryset, many=False)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    # Done--->


# Individuals properties
# Sellers can see their properties


# class SellerPropertyListView(ModelViewSet):
#     serializer_class = PropertySerializer
#     permission_classes = [IsAuthenticated, ]
#     http_method_names = ['get', ]

#     def get_queryset(self):
#         user = self.request.user
#         return Property.objects.filter(added_by__user=user)

#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(
#             queryset, many=True
#         )
#         return Response(serializer.data,
#                         status=status.HTTP_200_OK)

#     def retrieve(self, request, pk=None, *args, **kwargs):
#         queryset = self.get_queryset(request)
#         queryset = get_object_or_404(queryset, pk=pk)
#         serializer = self.get_serializer(queryset, many=False)
#         return Response(serializer.data,
#                         status=status.HTTP_200_OK)


# class SellerPropertyUpdateView(ModelViewSet):
#     serializer_class = PropertySerializer
#     permission_classes = ()
#     http_method_names = ["get", "put", "delete"]

#     def get_queryset(self):
#         user = self.request.user
#         ownerQuery = Seller.objects.get(id=1)
#         return Property.objects.filter(added_by=ownerQuery)

#     def retrieve(self, request, pk=None, *args, **kwargs):
#         queryset = self.get_queryset()
#         property = get_object_or_404(queryset, pk=pk)
#         serializer = self.get_serializer(
#             property)

#         return Response(serializer.data)

#     def update(self, request, pk=None, *args, **kwargs):
#         queryset = self.get_queryset()
#         property = get_object_or_404(queryset, pk=pk)
#         serializer = self.get_serializer(
#             instance=property, data=request.data
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk=None, *args, **kwargs):
#         queryset = self.get_queryset()
#         property = get_object_or_404(queryset, pk=pk)
#         property.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
