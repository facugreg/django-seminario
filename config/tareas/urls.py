from django.urls import path
from .views import TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView

urlpatterns = [
    path('', TareaListView.as_view(), name='lista'),
    path('crear/', TareaCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', TareaUpdateView.as_view(), name='editar'),
    path('borrar/<int:pk>/', TareaDeleteView.as_view(), name='borrar'),
]