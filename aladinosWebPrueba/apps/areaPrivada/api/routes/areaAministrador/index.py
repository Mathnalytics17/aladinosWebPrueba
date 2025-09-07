# urls.py
from django.urls import path
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.areaPrivada.api.views.areaAministrador.index import LlamadaViewSet
from apps.areaPrivada.api.views.areaAministrador.index import register_trazability_entry,register_trazability_exit,trazability_list

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
    path('trazability/', trazability_list, name='trazability-list'),
    path('trazability/register_entry/', register_trazability_entry, name='trazability-register-entry'),
    path('trazability/register_exit/', register_trazability_exit, name='trazability-register-exit'),
]
