from django.db import models
from sucursales.models import SucursalTrabajador
# Create your models here.
class AsistenciaTrabajador(models.Model):
	trabajador = models.ForeignKey(SucursalTrabajador)
	hora_ingreso = models.DateTimeField(null = True)
	hora_salida = models.DateTimeField(null=True)
	justificacion = models.TextField(max_length=400,blank=True, null = True)