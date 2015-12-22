from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


from sucursales.utilidades import Utilidades
from productos.models import Producto
import propiedades as Constante



# Create your models here.

class Almacen(models.Model):
    nombre_empresa = models.CharField(max_length=80)
    logo = models.ImageField(upload_to='empresa/',blank=True,null=True)
    ruc = models.CharField(unique=True, max_length = 11,validators=[ RegexValidator(regex = '\d{11}', message="Ruc no tiene 11 digitos", code="invalido")])
    todos_departamento = (('Ama','Amazonas'), ('Anc','Ancash'),('Apu','Apurimac'),('Are','Arequipa'),('Aya','Ayacucho'),('Caj','Cajamarca'),('Cal','Callao'),('Cuz','Cuzco'),('Hua','Huancavelica'),('Hun','Huanuco'),('Ica','Ica'),('Jun','Junin'),('Lal','La Libertad'),('Lam','Lambayeque'),('Lim','Lima'),('Lor','Loreto'),('Mad','Madre de Dios'),('Moq','Moquegua'),('Pas','Pasco'),('Piu','Piura'),('Pun','Puno'),('San','San Martin'),('Piu','Piura'),('Tac','Tacna'),('Tum','Tumbes'),('Uca','Ucayali'),)
    departamento = models.CharField(max_length=20, choices=todos_departamento, default='Lim')
    direccion = models.CharField(max_length=80)
    fecha_registro = models.DateTimeField(auto_now=True, editable=False)
    telefono = models.CharField(max_length=20)
    celular = models.CharField(max_length=20)
    descripcion = models.TextField(max_length=400)
    def clean(self):
        self.nombre_empresa = self.nombre_empresa.capitalize()
        validate_only_one_instance(self, Constante.CANTIDAD_EMPRESA)

    class Meta:
        verbose_name="Empresa"
    def __unicode__(self):
        return u'%s' % (self.nombre_empresa)		

class DetalleAlmacen(models.Model):
	id_almacen = models.ForeignKey(Almacen) 
	producto_id = models.ForeignKey(Producto)
	stock = models.PositiveIntegerField(default=0)
	adicional_stock = models.PositiveSmallIntegerField(default=0)
	descripcion = models.TextField(max_length=400)
	fecha_ingreso = models.DateTimeField(auto_now=True ,editable=False)
	class Meta:
		unique_together = ('producto_id',)
		verbose_name='Almacen Principal'
		verbose_name_plural = verbose_name

	def save(self):
		agregar = Utilidades().validarIngresoNum(self.adicional_stock)
		if agregar != 0 :
			stock_antes = self.stock
			self.stock += agregar
			self.adicional_stock = 0
			super(DetalleAlmacen, self).save()
			try:
				HistorialDetalleAlmacen.objects.create(
					adicional_producto = agregar,
					stock_actual = stock_antes,
					detalle_almacen_id = self
				)
			except Exception, e:
				print '%s' %(e)
		else:
			super(DetalleAlmacen, self).save()

class HistorialDetalleAlmacen(models.Model):
	adicional_producto = models.PositiveIntegerField()
	stock_actual = models.PositiveIntegerField()
	fecha_ingreso = models.DateTimeField(auto_now=True , editable=False)
	detalle_almacen_id = models.ForeignKey(DetalleAlmacen)
	#sucursal_id = models.ForeignKey(Sucursal, null=True)

def validate_only_one_instance(obj,cantidad):
    model = obj.__class__
    if (model.objects.count() >= cantidad and
            obj.id != model.objects.get().id):
        raise ValidationError("Puede solo crear maximo %d, %s." % (cantidad,model.__name__))
