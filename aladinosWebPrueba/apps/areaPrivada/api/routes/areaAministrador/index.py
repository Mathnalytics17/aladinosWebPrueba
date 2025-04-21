# urls.py
from django.urls import path
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.areaPrivada.api.views.areaAministrador.index import LlamadaViewSet

llamada_list = LlamadaViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

llamada_detail = LlamadaViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', llamada_list, name='llamada-list'),
    path('<int:pk>/', llamada_detail, name='llamada-detail'),
]
