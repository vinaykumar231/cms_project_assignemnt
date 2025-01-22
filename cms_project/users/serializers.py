from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'phone', 'address',
                 'city', 'state', 'country', 'pincode', 'role')
        read_only_fields = ('role',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'phone', 'address',
                 'city', 'state', 'country', 'pincode')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['email'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            address=validated_data.get('address', ''),
            city=validated_data.get('city', ''),
            state=validated_data.get('state', ''),
            country=validated_data.get('country', ''),
            pincode=validated_data['pincode']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
