from django.urls import path
from .views import TareaListView, TareaCreateView, TareaUpdateView, TareaDeleteView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', TareaListView.as_view(), name='lista'),
    path('crear/', TareaCreateView.as_view(), name='crear'),
    path('editar/<int:pk>/', TareaUpdateView.as_view(), name='editar'),
    path('borrar/<int:pk>/', TareaDeleteView.as_view(), name='borrar'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]