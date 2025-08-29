from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .throttling import LoginRateThrottle, PasswordResetRateThrottle
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)
from .redis_utils import generate_password_reset_token, validate_password_reset_token

User = get_user_model()


class UserRegistrationView(APIView):
    """API view for user registration."""
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'full_name', 'password', 'password_confirm'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email address'),
                'full_name': openapi.Schema(type=openapi.TYPE_STRING, description='User full name'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='User password'),
                'password_confirm': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD, description='Password confirmation'),
            }
        ),
        responses={
            201: openapi.Response(
                description="User registered successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        ),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            400: "Bad Request"
        }
    )
    def post(self, request):
        """
        Register a new user.
        
        Parameters:
        - email: User's email address (will be used as username)
        - full_name: User's full name
        - password: User's password
        - password_confirm: Confirmation of user's password
        
        Returns:
        - user: User information (id, email, full_name)
        - refresh: JWT refresh token
        - access: JWT access token
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """API view for user login."""
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Response('Login successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user': openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                            'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                        }
                    ),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            401: 'Invalid credentials'
        },
        operation_description="Login with email and password to receive JWT tokens"
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            response_data = {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    """API view for user profile."""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: openapi.Response('User profile', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format='email'),
                    'full_name': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            401: 'Authentication required'
        },
        operation_description="Get the profile information for the currently authenticated user. Requires authentication with a valid JWT token.",
        security=[{'Bearer': []}],
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description='JWT token in format: "Bearer eyJ0eXAi..." (include the word "Bearer" followed by a space, then the token)',
                type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def get(self, request):
        # Debug authentication
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        # Check if user is authenticated regardless of header
        if not request.user.is_authenticated:
            return Response({
                'detail': 'Authentication credentials were not provided.',
                'received_header': auth_header,
                'hint': 'Make sure you are providing the token with format: Bearer <token>'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # If we got here, authentication worked
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthDebugView(APIView):
    """Debug view to help with authentication issues."""
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        responses={
            200: openapi.Response('Authentication debug info', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'headers': openapi.Schema(type=openapi.TYPE_OBJECT),
                    'auth_header': openapi.Schema(type=openapi.TYPE_STRING),
                    'user': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ))
        },
        operation_description="Debug endpoint to troubleshoot authentication issues",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description='JWT token in format: "Bearer eyJ0eXAi..." (include the word "Bearer" followed by a space, then the token)',
                type=openapi.TYPE_STRING,
                required=False
            )
        ]
    )
    def get(self, request):
        # Get all headers for debugging
        headers = {k: v for k, v in request.META.items() if k.startswith('HTTP_')}
        auth_header = request.META.get('HTTP_AUTHORIZATION', 'Not found')
        
        # Check if user is authenticated
        if request.user.is_authenticated:
            user_info = f"Authenticated as: {request.user.email} (ID: {request.user.id})"
        else:
            user_info = "Not authenticated"
        
        return Response({
            'headers': headers,
            'auth_header': auth_header,
            'user': user_info,
        }, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        operation_description="Debug authentication issues. Provide your token and this will show you how to format it correctly.",
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description='Your raw JWT token',
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: 'Authentication debug information'
        }
    )
    def get(self, request):
        token = request.query_params.get('token', '')
        if not token:
            return Response({
                'error': 'Please provide a token as a query parameter',
                'example': '/api/v1/auth-debug/?token=your_jwt_token_here'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        return Response({
            'proper_header_value': f'Bearer {token}',
            'instructions': 'Use the value above in the Authorization header',
            'swagger_instructions': 'In Swagger UI, click the "Authorize" button and enter the value above'
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """API view for requesting a password reset."""
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    @swagger_auto_schema(
        request_body=PasswordResetRequestSerializer,
        responses={
            200: openapi.Response('Password reset token generated', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: 'Invalid request',
            500: 'Server error'
        },
        operation_description="Request a password reset token by providing your email address"
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
                try:
                    # Generate and store token in Redis or Django cache
                    token = generate_password_reset_token(user.id)
                    
                    # In a real-world application, you would send an email with the reset link
                    # For this project, we'll just return the token in the response
                    return Response({
                        'detail': 'Password reset token generated successfully.',
                        'token': token
                    }, status=status.HTTP_200_OK)
                except Exception as e:
                    # Log the error but don't expose details to the client
                    import logging
                    logger = logging.getLogger(__name__)
                    logger.error(f"Password reset token generation failed: {str(e)}")
                    return Response({
                        'detail': 'Could not generate password reset token. Please try again later.'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except User.DoesNotExist:
                # Don't reveal whether a user exists or not for security
                pass
            
            return Response({
                'detail': 'If the email exists in our system, a password reset link will be sent.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    """API view for confirming a password reset."""
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    @swagger_auto_schema(
        request_body=PasswordResetConfirmSerializer,
        responses={
            200: openapi.Response('Password reset successful', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: 'Invalid token or passwords do not match',
            500: 'Server error'
        },
        operation_description="Reset your password using the token received from the reset request"
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                # Validate token from Redis or Django cache
                user_id = validate_password_reset_token(token)
                
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        user.set_password(new_password)
                        user.save()
                        
                        return Response({
                            'detail': 'Password reset successful. You can now log in with your new password.'
                        }, status=status.HTTP_200_OK)
                    except User.DoesNotExist:
                        pass
                
                return Response({
                    'detail': 'Invalid or expired token. Please request a new password reset.'
                }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                # Log the error but don't expose details to the client
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Password reset confirmation failed: {str(e)}")
                return Response({
                    'detail': 'An error occurred during password reset. Please try again later.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
