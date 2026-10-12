from django.db import models


class Tarea(models.Model):
    class Prioridad(models.TextChoices):
        ALTA = "A", "Alta"
        MEDIA = "M", "Media"
        BAJA = "B", "Baja"

    titulo = models.CharField("título", max_length=100)
    descripcion = models.TextField("descripción", blank=True)
    prioridad = models.CharField(max_length=1, choices=Prioridad.choices, default=Prioridad.MEDIA)
    fecha_limite = models.DateField("fecha límite", null=True, blank=True)
    completada = models.BooleanField(default=False)
    creada = models.DateTimeField(auto_now_add=True)

    #horas_estimadas = models.PositiveIntegerField("horas estimadas", null=True, blank=True)
    #py manage.py makemigrations
    #py manage.py migrate

    class Meta:
        ordering = ["completada", "fecha_limite"]

    def __str__(self):
        return self.titulo
