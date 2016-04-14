from django.db import models
from django.core.validators import RegexValidator
# Create your models here.
#Modelo Cliente  , no deberia estar  aqui pero por el momento

class Cliente(models.Model):
	razon_social_nombre = models.CharField(max_length = 70)
	#nombre = models.CharField(max_length=50)
	#apellidos = models.CharField(max_length=50)
	telefono = models.CharField(max_length=15, blank=True , null=True)
	ruc_dni = models.CharField(unique=True, max_length = 8 ,validators=[ RegexValidator(regex = '\d{8}', message="DNI no tiene 8 digitos", code="invalido")])
	direccion = models.CharField(max_length=70 , blank=True, null=True,)	
	#ruc = models.CharField(max_length=11 , blank=True)
	correo = models.EmailField( max_length='200')
	#Segun lo pedido debe de existir 2 tipos de cliente-Lima/Provincia
	tipo_cliente_all = (('Lim', 'Lima'),('Pro', 'Provincia'),)
	tipo_cliente = models.CharField(max_length=20, choices=tipo_cliente_all, default='Lim')
	def clean(self):
		self.razon_social_nombre = self.razon_social_nombre.capitalize()
		self.direccion = self.direccion.capitalize()
		#self.correo = self.correo.lowercase()

	def __unicode__(self):
		return "Cliente : [%s] %s %s " %(self.razon_social_nombre,self.ruc_dni , self.correo)
