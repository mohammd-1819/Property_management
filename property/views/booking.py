from ..models import VisitBooking
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import VisitBookingSerializer, CreateBookingSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class BookingListView(APIView, Pagination):
    permission_classes = (IsAdminUser,)
    serializer_class = VisitBookingSerializer

    @extend_schema(
        tags=['Booking'],
        summary='List of booking requests (Admin Users)'
    )
    def get(self, request):
        bookings = VisitBooking.objects.all()
        result = self.paginate_queryset(bookings, request)
        serializer = VisitBookingSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class BookingDetailView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = VisitBookingSerializer

    @extend_schema(
        tags=['Booking'],
        summary='Details of a single booking request (Admin Users)'
    )
    def get(self, request, booking_id):
        try:
            booking_request = VisitBooking.objects.get(id=booking_id)
        except VisitBooking.DoesNotExist:
            return Response({'error': 'Request Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VisitBookingSerializer(booking_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateBookingRequestView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = VisitBookingSerializer

    @extend_schema(
        tags=['Booking'],
        summary='Update a booking request (Admin users)'
    )
    def put(self, request, booking_id):
        try:
            booking_request = VisitBooking.objects.get(id=booking_id)
        except VisitBooking.DoesNotExist:
            return Response({'error': 'Request Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VisitBookingSerializer(instance=booking_request, data=request.data, partial=True)
        return Response({'message': 'Booking Request Updated', 'result': serializer.data}, status=status.HTTP_200_OK)


class CreateBookingRequestView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateBookingSerializer

    @extend_schema(
        tags=['Booking'],
        summary='Send a booking request'
    )
    def post(self, request):
        serializer = CreateBookingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'booking Request Sent', 'result': serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveBookingRequestView(APIView):
    permission_classes = (IsAdminUser,)
    serializer_class = VisitBookingSerializer

    @extend_schema(
        tags=['Booking'],
        summary='Remove a booking request (Admin Users)'
    )
    def delete(self, request, booking_id):
        try:
            booking_request = VisitBooking.objects.get(id=booking_id)
        except VisitBooking.DoesNotExist:
            return Response({'error': 'Request Not Found'}, status=status.HTTP_404_NOT_FOUND)

        booking_request.delete()
        return Response({'message': 'Booking Request Removed'}, status=status.HTTP_200_OK)
