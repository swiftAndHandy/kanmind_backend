from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        data = dict(serializer.data)
        data['token'] = token.key
        data['user_id'] = user.id


        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get('email'), password=request.data.get('password'))

        if user is None:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "token": Token.objects.get(user=user).key,
            "fullname": user.fullname,
            "email": user.email,
            "user_id": user.id
        }, status=status.HTTP_200_OK)