from django.shortcuts import render
from rest_framework import mixins, viewsets
from django.contrib.auth import get_user_model
from users.serializers import RegisterSerializer, PasswordSerializer, PasswordResetConfirmSerializer, EmailCodeResendSerializer, EmailCodeConfirmSerializer
from rest_framework.decorators import action
from users.models import EmailVerification
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.response import Response
import random
from datetime import timedelta
from rest_framework import status, serializers
from rest_framework.status import HTTP_204_NO_CONTENT
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
User = get_user_model()



class UserListDetailViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            self.send_verification_code(user)
            return Response({"detail":"User registered succesfully and verification code sent to email"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def send_verification_code(self, user):
        code = str(random.randint(100000, 999999))

        EmailVerification.objects.update_or_create(
            user=user,
            defaults = {"code":code, "created_at": timezone.now()}
        )
        subject = 'your verification code'
        message = f"hello {user.username}, your verification code is {code}"
        send_mail(subject, message, 'no-reply@example.com', [user.email])

    @action(detail=False, methods=["post"], url_path="resend_code", serializer_class=EmailCodeResendSerializer)
    def resend_code(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data["user"]
        existing = EmailVerification.objects.filter(user=user).first()
        if existing:
            time_diff = timezone.now() - existing.created_at
            if time_diff < timedelta(minutes=1):
                wait_seconds = 60 - int(time_diff.total_second())
                return Response(
                    {"detail":f"please wait {wait_seconds} seconds before requesting new code."},   
                    status = 429
                )
            
        self.send_verification_code(user)
        return Response({"detail":"Verification code resent succesfully"})
    
    @action(detail=False, methods=['post'], url_path='confirm_code', serializer_class=EmailCodeConfirmSerializer)
    def confirm_code(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_active = True
            user.save()
            return Response({"message": 'user was successfully activated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordSerializer
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            #Token Generation

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            #Password reset URL generation

            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={"uidb64":uid, "token":token})
            )

            #send mail
            subject = "password reset"
            message = f"click the link to reset password {reset_url}"
            send_mail(subject, message, 'no-reply@example.com', [user.email])

            return Response(
                {"message": "link successfully sent to email"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = PasswordResetConfirmSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uidb64', openapi.IN_PATH, description="User ID (base64 encoded)", type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_PATH, description="Password reset token", type=openapi.TYPE_STRING),
        ]
    )

    def create(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message":"Password succesfully updated"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            access = response.data.get('access')
            response.set_cookie(
                key='jwt_token',
                value=access,
                httponly=True,
                samesite='Lax',
                secure=False,  
            )
        return response
    

class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        response = Response({"message":"logged out succesfully"})
        response.delete_cookie("jwt_token")
        return response