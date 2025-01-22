from django.core.cache import cache
from rest_framework.renderers import JSONRenderer

from ..models import Property
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import PropertySerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class PropertyListView(APIView, Pagination):
    permission_classes = (AllowAny,)
    serializer_class = PropertySerializer

    @extend_schema(
        tags=['Property'],
        summary='List of All Properties',
        auth=[],
    )
    def get(self, request):
        page = request.GET.get("page", 1)
        cache_key = f'property_list_page_{page}'

        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        properties = Property.objects.all()
        result = self.paginate_queryset(properties, request)
        serializer = PropertySerializer(result, many=True, context={'request': request})
        response = self.get_paginated_response(serializer.data)

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()

        cache.set(cache_key, response, 60 * 15)
        return response


class PropertyDetailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = PropertySerializer

    @extend_schema(
        tags=['Property'],
        summary='Details of a Single Property',
        auth=[]
    )
    def get(self, request, property_title):
        try:
            instance = Property.objects.get(title=property_title)
        except Property.DoesNotExist:
            return Response({'error': 'Property Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertySerializer(instance=instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePropertyView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer

    @extend_schema(
        tags=['Property'],
        summary='Create a new Property'
    )
    def post(self, request):
        print(request)
        print(request.build_absolute_uri('/'))
        serializer = PropertySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Property added', 'result': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PropertyUpdateView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer

    @extend_schema(
        tags=['Property'],
        summary='Update a Property'
    )
    def put(self, request, property_title):
        try:
            instance = Property.objects.get(title=property_title)
        except Property.DoesNotExist:
            return Response({'error': 'Property Not Found'}, status=status.HTTP_404_NOT_FOUND)

        if instance.owner != request.user:
            return Response({"error": "You do not have permission to edit this Property."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PropertySerializer(instance=instance, data=request.data, partial=True,
                                        context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Property Updated Successfully', 'result': serializer.data},
                            status=status.HTTP_200_OK)


class DeletePropertyView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer

    @extend_schema(
        tags=['Property'],
        summary='Delete a Property'
    )
    def delete(self, request, property_title):
        try:
            instance = Property.objects.get(title=property_title)
        except Property.DoesNotExist:
            return Response({'error': 'Property Not Found'}, status=status.HTTP_404_NOT_FOUND)

        instance.delete()
        return Response({'message': 'Property Deleted'}, status=status.HTTP_200_OK)
