from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from apps.areaPrivada.api.models.users.index import EmailVerificationToken, PasswordResetToken,Socio
from apps.areaPrivada.api.serializers.users.index import (
    UserRegistrationSerializer, 
    CustomTokenObtainPairSerializer,
    UserSerializer, 
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer,SocioSerializer,UserDetailSerializer
)
from django.shortcuts import get_object_or_404
from permissions import IsAdmin, IsJefe, IsComercial
from datetime import timedelta
import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers, permissions

from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth import get_user_model
from apps.areaPrivada.api.serializers.users.index import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta


logger = logging.getLogger(__name__)
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    Vista para registro de nuevos usuarios con verificación por email
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            user = serializer.save(is_active=False)  # Usuario inactivo hasta verificación
            self._send_verification_email(user)
        except Exception as e:
            logger.error(f"Error en registro de usuario: {str(e)}")
            raise

    def _send_verification_email(self, user):
        """Envía email de verificación con token"""
        try:
            # Eliminar tokens previos si existen
            EmailVerificationToken.objects.filter(user=user).delete()
            
            expires_at = timezone.now() + timedelta(days=settings.EMAIL_VERIFICATION_TOKEN_EXPIRY_DAYS)
            token = EmailVerificationToken.objects.create(
                user=user,
                expires_at=expires_at
            )
            
            verification_url = f"{settings.FRONTEND_URL}areaPrivada/users/confirmUser?token={token.token}"
            subject = "Verifica tu correo electrónico"
            message = f"""
            Hola {user.get_full_name() or user.email},
            
            Por favor haz clic en el siguiente enlace para verificar tu correo:
            {verification_url}
            
            Este enlace expirará en {settings.EMAIL_VERIFICATION_TOKEN_EXPIRY_DAYS} días.
            
            Si no solicitaste este registro, ignora este mensaje.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"Error enviando email de verificación: {str(e)}")
            raise

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

class UserViewSet(viewsets.ModelViewSet):
    """
    Vista para gestión de usuarios con permisos diferenciados
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    def get_permissions(self):
        """
        Asigna permisos según la acción:
        - Crear/Eliminar: Solo Admin
        - Actualizar: Admin o Jefe
        - Leer: Cualquier usuario autenticado
        """
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAdmin | IsJefe]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obtener datos del usuario actual"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Endpoint para cambiar contraseña"""
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {"detail": "La contraseña actual es incorrecta"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Invalidate all tokens after password change
        user.auth_token_set.all().delete()
        
        return Response({"status": "Contraseña actualizada correctamente"})
    
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Lógica adicional antes de eliminar (opcional)
        if instance == self.request.user:
            return Response(
                {"error": "No puedes eliminarte a ti mismo"},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
class EmailVerificationView(generics.GenericAPIView):
    """
    Vista para verificación de email mediante token
    """
    serializer_class = EmailVerificationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = EmailVerificationToken.objects.get(token=serializer.validated_data['token'])
            if not token.is_valid():
                return Response(
                    {"detail": "El enlace de verificación ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user = token.user
            if user.email_verified:
                return Response(
                    {"detail": "El email ya ha sido verificado anteriormente"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user.email_verified = True
            user.is_active = True
            user.save()
            token.delete()
            
            return Response({"status": "Email verificado correctamente"})
            
        except EmailVerificationToken.DoesNotExist:
            return Response(
                {"detail": "Token de verificación inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )

class PasswordResetRequestView(generics.GenericAPIView):
    """
    Vista para solicitar reseteo de contraseña
    """
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Eliminar tokens previos
            PasswordResetToken.objects.filter(user=user).delete()
            
            expires_at = timezone.now() + timedelta(hours=settings.PASSWORD_RESET_TOKEN_EXPIRY_HOURS)
            token = PasswordResetToken.objects.create(
                user=user,
                expires_at=expires_at
            )
            
            reset_url = f"{settings.FRONTEND_URL}/auth/reset-password/{token.token}/"
            subject = "Restablecer tu contraseña"
            message = f"""
            Hola {user.get_full_name() or user.email},
            
            Para restablecer tu contraseña, haz clic en el siguiente enlace:
            {reset_url}
            
            Este enlace expirará en {settings.PASSWORD_RESET_TOKEN_EXPIRY_HOURS} horas.
            
            Si no solicitaste este cambio, ignora este mensaje.
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            
            return Response({"status": "Email de recuperación enviado"})
            
        except User.DoesNotExist:
            # No revelar que el email no existe por seguridad
            return Response({"status": "Si el email existe, se ha enviado un enlace de recuperación"})

class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Vista para confirmar reseteo de contraseña con token
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            token = PasswordResetToken.objects.get(token=serializer.validated_data['token'])
            if not token.is_valid():
                return Response(
                    {"detail": "El enlace de recuperación ha expirado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
            user = token.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            token.delete()
            
            # Invalidar todos los tokens de sesión
            user.auth_token_set.all().delete()
            
            return Response({"status": "Contraseña restablecida correctamente"})
            
        except PasswordResetToken.DoesNotExist:
            return Response(
                {"detail": "Token de recuperación inválido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

User = get_user_model()

class CurrentUserView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend


from django.db import transaction

class SocioViewSet(viewsets.ModelViewSet):
    serializer_class = SocioSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['fundraiser']

    def get_queryset(self):
        queryset = Socio.objects.all()
        fundraiser_id = self.request.query_params.get('fundraiser_id')

        if fundraiser_id:
            try:
                queryset = queryset.filter(fundraiser_id=int(fundraiser_id))
            except (ValueError, TypeError):
                return Socio.objects.none()
        
        return queryset

    def create(self, request, *args, **kwargs):
        # Si se recibe una lista de objetos
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Comportamiento normal (un solo objeto)
            return super().create(request, *args, **kwargs)

    def perform_bulk_create(self, serializer):
        serializer.save()


class SocioDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get_object(self, pk):
        """
        Helper method para obtener el socio sin validación de pertenencia
        """
        return get_object_or_404(Socio, pk=pk)  # Eliminamos la validación de permiso

    def get(self, request, pk):
        """
        Obtiene un socio específico por ID
        """
        socio = self.get_object(pk)
        serializer = SocioSerializer(socio)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Actualiza completamente un socio
        """
        socio = self.get_object(pk)
        serializer = SocioSerializer(socio, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        Actualiza parcialmente un socio
        """
        socio = self.get_object(pk)
        serializer = SocioSerializer(socio, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Elimina un socio
        """
        socio = self.get_object(pk)
        socio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



