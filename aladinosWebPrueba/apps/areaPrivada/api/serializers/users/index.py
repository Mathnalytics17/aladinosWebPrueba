# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.areaPrivada.api.models.users.index  import EmailVerificationToken, PasswordResetToken,Socio,Fundraiser
import uuid
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework import serializers



User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'first_name', 'last_name', 'phone','role','fundRaiserCode']
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        try:
            validate_password(attrs['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['is_active'] = user.is_active
        token['email_verified'] = user.email_verified
        
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        
        if not self.user.is_active:
            raise serializers.ValidationError("User account is not active.")
            
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'phone', 'is_active', 'email_verified','fundRaiserCode']
        read_only_fields = ['id', 'email', 'is_active', 'email_verified','fundRaiserCode']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'is_active', 'role', 'email_verified', 'date_joined','fundRaiserCode']
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'read_only': True}
        }

    def update(self, instance, validated_data):
        # Evitar que se actualice el username
        validated_data.pop('username', None)
        return super().update(instance, validated_data)
    
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        try:
            validate_password(attrs['new_password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})

        return attrs

class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})

        try:
            validate_password(attrs['new_password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})

        return attrs
    


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'email_verified','fundRaiserCode']
        read_only_fields = ['id', 'email', 'role', 'is_active', 'email_verified','fundRaiserCode']
        
class SocioSerializer(serializers.ModelSerializer):
    # Este se usa al hacer POST/PUT (envías el ID del fundraiser)
    fundraiser = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='COMERCIAL'),
        write_only=True
    )

    # Este se usa al hacer GET (muestra los detalles del fundraiser)
    fundraiser_data = UserSerializer(source='fundraiser', read_only=True)

    class Meta:
        model = Socio
        fields = '__all__'  # incluye todo, incluido fundraiser y fundraiser_data

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Unificamos para que el frontend reciba solo `fundraiser` con info completa
        rep['fundraiser'] = rep.pop('fundraiser_data', None)
        return rep

class FundraiserSerializer(serializers.ModelSerializer):
    # Muestra el username del usuario en lugar del ID
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )

    class Meta:
        model = Fundraiser
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'fundraiser_code': {'required': True},
        }