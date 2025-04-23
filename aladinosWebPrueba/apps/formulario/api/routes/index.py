from django.urls import path
from apps.formulario.api.views.index import FormularioCreateView,FormularioGoogleSheetsView,FormularioViewSet

urlpatterns = [
  path('', FormularioCreateView.as_view(), name='formulario-create'),
  path('guardarBorrador/', FormularioGoogleSheetsView.as_view(), name='formulario-borrador'),
  path('formularioRows/',FormularioViewSet.as_view({'get': 'list'}), name='formulario-borrador'),
  
]