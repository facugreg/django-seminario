from django.contrib import admin
from .models import Tarea

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "prioridad", "fecha_limite", "completada"]
    list_filter = ["prioridad", "completada"]
    search_fields = ["titulo", "descripcion"]
    list_editable = ["completada"]


    #Tarea.objects.filter(prioridad="A")        
    #print(Tarea.objects.filter(prioridad="A").query)                                     