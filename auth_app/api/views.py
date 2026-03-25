from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_app.api.serializers import RegistrationSerializer, UserProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, NotFound


from auth_app.models import UserProfile


class RegistrationView(APIView):
    """
    Public POST only view.
    Creates new user with given credentials.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        # dict is required, to make serializer.data mutable to extend the Response.
        data = dict(serializer.data)
        data['token'] = token.key
        data['user_id'] = user.id

        return Response(data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    """
    Public POST only view.
    Checks email and password to authenticate user.
    """
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

class UserProfileView(generics.ListAPIView):
    """
    To prevent data-leaks, only Authenticated users can check E-Mail/User connectivity.
    Required to add Users as Board Members by entering an e-mail address.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.query_params.get('email')

        try:
            validate_email(email)
        except DjangoValidationError:
            raise ValidationError({'email': 'Email is missing or invalid format.'})

        user = UserProfile.objects.filter(email__iexact=email)

        if user:
            return user

        raise NotFound({'email': 'Email not found.'})