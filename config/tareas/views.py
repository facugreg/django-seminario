from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Tarea
from django import forms

class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/tarea_list.html'


class FechaWidgetMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha_limite'].widget = forms.DateInput(
            attrs={'type': 'date'},
            format='%Y-%m-%d'
        )
        return form



class TareaCreateView(FechaWidgetMixin,LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'prioridad', 'fecha_limite', 'completada']
    template_name = 'tareas/tarea_form.html'
    permission_required = 'tareas.add_tarea'  
    success_url = reverse_lazy('lista')


class TareaUpdateView(FechaWidgetMixin,LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'prioridad', 'fecha_limite', 'completada']
    template_name = 'tareas/tarea_form.html'
    permission_required = 'tareas.change_tarea'
    success_url = reverse_lazy('lista')


class TareaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Tarea
    template_name = 'tareas/tarea_confirm_delete.html'
    permission_required = 'tareas.delete_tarea'
    success_url = reverse_lazy('lista')