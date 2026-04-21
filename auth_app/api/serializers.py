from rest_framework import serializers

from auth_app.models import UserProfile


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile
        fields = ['fullname', 'email', 'password', 'repeated_password']

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError('Passwords must match')
        data.pop('repeated_password')
        data['email'] = data['email'].lower()
        return data

    def create(self, validated_data):
        # pop password before create() to prevent storing plaintext in DB
        password = validated_data.pop('password')
        user = UserProfile.objects.create(**validated_data)
        # hash and save password
        user.set_password(password)
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'fullname']