from rest_framework import status
from rest_framework.renderers import JSONRenderer

from .serializers import SignUpSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from property.models import Property
from property.serializers import PropertySerializer
from .pagination import Pagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.core.cache import cache


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @extend_schema(
        tags=['Sign-Up'],
        responses={200: SignUpSerializer},
        auth=[]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                'message': 'Signup Successful',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['User'],
        summary='User Profile'
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['User'],
        summary='Update User Profile'
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile Updated', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPropertyView(APIView, Pagination):
    permission_classes = (IsAuthenticated,)
    serializer_class = PropertySerializer

    @method_decorator(vary_on_headers("Authorization"))
    @extend_schema(
        tags=['User'],
        summary='List of user properties'
    )
    def get(self, request):
        user_id = request.user.id
        page = request.GET.get("page", 1)
        cache_key = f"user_property_list_page_{page}_user_{user_id}"

        cached_response = cache.get(cache_key)
        if cached_response:
            return cached_response

        properties = Property.objects.filter(owner__user=request.user)
        result = self.paginate_queryset(properties, request)
        serializer = PropertySerializer(result, many=True, context={'request': request})
        response = self.get_paginated_response(serializer.data)

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        response.render()

        cache.set(cache_key, response, 60 * 15)
        return response
