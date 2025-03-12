from django.urls import path
from apps.formulario.api.views.index import FormularioCreateView

urlpatterns = [
  path('', FormularioCreateView.as_view(), name='formulario-create'),
]