from ..models import City
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import CitySerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class CityListView(APIView, Pagination):
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    @extend_schema(
        tags=['City'],
        summary='List of al cities',
        auth=[]
    )
    def get(self, request):
        cities = City.objects.all()
        result = self.paginate_queryset(cities, request)
        serializer = CitySerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class CityDetailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CitySerializer

    @extend_schema(
        tags=['City'],
        summary='Details of a single city',
        auth=[]
    )
    def get(self, request, city_name):
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response({'error': 'City Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(instance=city)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCityView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CitySerializer

    @extend_schema(
        tags=['City'],
        summary='Add a new city'
    )
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'City Added', 'result': serializer.data}, status=status.HTTP_201_CREATED)


class UpdateCityView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CitySerializer

    @extend_schema(
        tags=['City'],
        summary='Update the details of a city'
    )
    def put(self, request, city_name):
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response({'error': 'City Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(instance=city, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'City Updated', 'result': serializer.data}, status=status.HTTP_200_OK)


class RemoveCityView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = CitySerializer

    @extend_schema(
        tags=['City'],
        summary='Remove a city'
    )
    def delete(self, request, city_name):
        try:
            city = City.objects.get(name=city_name)
        except City.DoesNotExist:
            return Response({'error': 'City Not Found'}, status=status.HTTP_404_NOT_FOUND)

        city.delete()
        return Response({'message': 'City Remove'}, status=status.HTTP_200_OK)
