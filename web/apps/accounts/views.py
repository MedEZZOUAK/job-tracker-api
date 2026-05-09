from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .serializers import RegisterSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserProfileSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class PasswordResetConfirmPageView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = None # Not an API view per se

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/password_reset_confirm.html')

    def post(self, request, *args, **kwargs):
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        uidb64 = request.query_params.get('uid')
        token = request.query_params.get('token')

        if password != confirm_password:
            return render(request, 'accounts/password_reset_confirm.html', {'error': 'Passwords do not match.'})

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'accounts/password_reset_confirm.html', {'error': 'Invalid reset link.'})

        if not default_token_generator.check_token(user, token):
            return render(request, 'accounts/password_reset_confirm.html', {'error': 'Invalid or expired token.'})

        try:
            validate_password(password, user)
        except ValidationError as e:
            return render(request, 'accounts/password_reset_confirm.html', {'error': e.messages[0]})

        user.set_password(password)
        user.save()
        return render(request, 'accounts/password_reset_confirm.html', {'success': True})

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Pointing to the new interactive page URL
        reset_link = f"http://app.localhost/reset-password/?uid={uid}&token={token}"
        
        send_mail(
            subject='Password Reset Request',
            message=f'Click the following link to reset your password: {reset_link}',
            from_email='noreply@jobtracker.local',
            recipient_list=[email],
            fail_silently=False,
        )
        
        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been successfully reset."}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
