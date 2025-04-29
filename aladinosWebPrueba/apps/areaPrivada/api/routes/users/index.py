# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from ...views.users.index import (
    UserRegistrationView, CustomTokenObtainPairView,
    UserViewSet, EmailVerificationView,
    ForgotPasswordView, PasswordResetConfirmView,CurrentUserView,SocioViewSet,SocioDetailView,UserDetailView,FundraiserViewSet,FundraiserDetailView
)
urlpatterns = [
   path('', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
    path('password-reset/', ForgotPasswordView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('socio/', SocioViewSet.as_view({'get': 'list', 'post': 'create'}), name='socio-list'),

    path('socio/<int:pk>/', SocioDetailView.as_view(), name='socio-detail'),
    path('fundraisers/', FundraiserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='fundraiser-list'),
    
    path('fundraisers/<int:pk>/', FundraiserDetailView.as_view(), name='fundraiser-detail'),
]
    
