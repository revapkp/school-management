from rest_framework.response import Response
from.serializers import LoginSerializer
from.models import *
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken







class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                    'is_admin': user.is_admin,
                    'is_office_staff': user.is_office_staff,
                    'is_librarian': user.is_librarian
                }, status=200)
            else:
                return Response({'detail': 'Account is not active'}, status=400)

        
        return Response({'detail': 'Invalid credentials'}, status=400)
