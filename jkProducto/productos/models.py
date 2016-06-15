# -*- encoding:utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError

#from django.contrib.auth.models import User
import propiedades as Constante
#from django.contrib.auth import get_user_model

# Create your models here.


def validate_only_one_instance(obj,cantidad):
    model = obj.__class__
    if (model.objects.count() >= cantidad and
            obj.id != model.objects.get().id):
        raise ValidationError("Puede solo crear maximo %d, %s." % (cantidad,model.__name__))


class TipoProducto(models.Model):
    nombre = models.CharField(max_length=60,unique=True)
#tipo_general = (('Cel','Celular'), ('Tab','Tablets'),)
#tipo_especifico = models.CharField(max_length=10, choices=tipo_general, default='Cel')
    class Meta:
		verbose_name_plural = "Tipos de Productos"
    def clean(self):
        self.nombre = self.nombre.capitalize()
    def __str__(self):
    	return self.nombre


class Marca(models.Model):
    nombre = models.CharField(max_length=60,unique=True)	
    def clean(self):
        self.nombre = self.nombre.capitalize()
    def __str__(self):
        return self.nombre


class Producto(models.Model):
	codigo = models.CharField(max_length=20)
	nombre_comercial = models.CharField(max_length=60)
	color_todos = (('Sc',''),('Az','Azul'), ('Bl','Blanco'), ('Ne','Negro'),('Ot','Otro'), ('Pl','Plomo'),)
	color = models.CharField(max_length=2, choices=color_todos, default='Ot')
	precio_x_mayor = models.DecimalField(max_digits=19,decimal_places=2)
	precio_x_menor = models.DecimalField(max_digits=19,decimal_places=2)	
	marca = models.ForeignKey(Marca)
	tipo_producto = models.ForeignKey(TipoProducto)
	#logo = models.ImageField(upload_to='fotos/',blank=True,null=True)
	imagen = models.ImageField(upload_to='productos/',blank=True,null=True, default='touchTactil.png')
	class Meta:
		verbose_name_plural = "Mantenimiento de Productos"
		unique_together = ('codigo', 'color','marca','tipo_producto')

	def clean(self):
		validate_only_one_instance(self, Constante.CANTIDAD_PRODUCTO)
	def __unicode__(self):
		return u'%s/%s/ color: %s/ Marca: %s/ Tipo: %s' % (self.nombre_comercial,self.codigo,self.get_color_display(),self.marca.nombre,self.tipo_producto.nombre)

"""
class ProductoAlmacen(models.Model):
	codigo =
	
	color_todos = (('Sc',''),('Az','Azul'), ('Bl','Blanco'), ('Ne','Negro'), ('Pl','Plomo'),)
	color = models.CharField(max_length=2, choices=color_todos, default='Sc')
	stock = models.PositiveSmallIntegerField(default=0)
	adicional = models.PositiveSmallIntegerField(default=0)
	mayor = models.PositiveSmallIntegerField()
	menor = models.PositiveSmallIntegerField()
	tipo_producto = models.ForeignKey(TipoProducto)
	fecha_ingreso = models.DateTimeField(auto_now=True)

        def save(self):
            self.stock += self.adicional
            self.adicional = 0
            super(ProductoAlmacen, self).save()


        def NuevoAlgo(self):
        	pass



	class Meta:
		unique_together = ('codigo', 'color',)
		
	def __unicode__(self):
		return "  %s , %s , %s, %s, %s, %s, %s"%(self.codigo ,self.marca,self.color,self.tipo_producto,self.stock,self.mayor,self.menor)

"""




#User._meta.get_field_by_name('email')[0]._unique = True
#User._meta.get_field_by_name('username')[0]._unique = True


