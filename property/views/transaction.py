from ..models import Transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from ..serializers import TransactionSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class TransactionListView(APIView, Pagination):
    permission_classes = (IsAdminUser,)
    serializer_class = TransactionSerializer

    @extend_schema(
        tags=['Transaction'],
        summary='List of all Transactions'
    )
    def get(self, request):
        transactions = Transaction.objects.all()
        result = self.paginate_queryset(transactions, request)
        serializer = TransactionSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class UserTransactionView(APIView, Pagination):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    @extend_schema(
        tags=['Transaction'],
        summary='User Transactions'
    )
    def get(self, request):
        user_transactions = Transaction.objects.filter(buyer=request.user)
        result = self.paginate_queryset(user_transactions, request)
        serializer = TransactionSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)


class CreateTransaction(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    @extend_schema(
        tags=['Transaction'],
        summary='Create New Transaction'
    )
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            property = serializer.validated_data['property']
            if not property.is_sold_or_rented:
                serializer.save()
                property.is_sold_or_rented = True
                property.save()
                return Response({'message': 'Transaction Created', 'result': serializer.data},
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'Property already sold or rented'}, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer

    @extend_schema(
        tags=['Transaction'],
        summary='Details of a single Transaction'
    )
    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
        except Transaction.DoesNotExist:
            return Response({'error': 'Transaction Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionSerializer(instance=transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
