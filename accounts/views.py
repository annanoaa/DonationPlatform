from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Create a new user account with the provided information",
        responses={
            201: openapi.Response(
                description="Successfully registered",
                schema=UserSerializer
            ),
            400: "Bad Request - Invalid data"
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description="Authenticate user and return JWT tokens",
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'tokens': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                                'access': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            401: "Invalid credentials"
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })

        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_summary="Get user profile",
        operation_description="Retrieve the profile of the currently authenticated user",
        responses={
            200: UserSerializer,
            401: "Authentication credentials were not provided"
        },
        tags=['User Profile']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update user profile",
        operation_description="Update the profile of the currently authenticated user",
        responses={
            200: UserSerializer,
            400: "Bad Request - Invalid data",
            401: "Authentication credentials were not provided"
        },
        tags=['User Profile']
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)