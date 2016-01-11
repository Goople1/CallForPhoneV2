from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from datetime import date
from productos.models import Producto
from almacen.models import Almacen
import propiedades as Constante



def validate_only_one_instance(obj,cantidad):
    model = obj.__class__
    if (model.objects.count() >= cantidad and
            obj.id != model.objects.get().id):
        raise ValidationError("Puede solo crear maximo %d, %s." % (cantidad,model.__name__))
#from utilidades import Utilidades
# Create your models here.
# class Almacen(models.Model):
#     nombre_empresa = models.CharField(max_length=80)
#     logo = models.ImageField(upload_to='empresa/',blank=True,null=True)
#     ruc = models.CharField(unique=True, max_length = 11,validators=[ RegexValidator(regex = '\d{11}', message="Ruc no tiene 11 digitos", code="invalido")])
#     todos_departamento = (('Ama','Amazonas'), ('Anc','Ancash'),('Apu','Apurimac'),('Are','Arequipa'),('Aya','Ayacucho'),('Caj','Cajamarca'),('Cal','Callao'),('Cuz','Cuzco'),('Hua','Huancavelica'),('Hun','Huanuco'),('Ica','Ica'),('Jun','Junin'),('Lal','La Libertad'),('Lam','Lambayeque'),('Lim','Lima'),('Lor','Loreto'),('Mad','Madre de Dios'),('Moq','Moquegua'),('Pas','Pasco'),('Piu','Piura'),('Pun','Puno'),('San','San Martin'),('Piu','Piura'),('Tac','Tacna'),('Tum','Tumbes'),('Uca','Ucayali'),)
#     departamento = models.CharField(max_length=20, choices=todos_departamento, default='Lim')
#     direccion = models.CharField(max_length=80)
#     fecha_registro = models.DateTimeField(auto_now=True, editable=False)
#     telefono = models.CharField(max_length=20)
#     celular = models.CharField(max_length=20)
#     descripcion = models.TextField(max_length=400)
#     def clean(self):
#         self.nombre_empresa = self.nombre_empresa.capitalize()
#     class Meta:
#         verbose_name="Empresa"
#     def __unicode__(self):
#         return u'%s' % (self.nombre_empresa)		

# class DetalleAlmacen(models.Model):
# 	id_almacen = models.ForeignKey(Almacen) 
# 	producto_id = models.ForeignKey(Producto)
# 	stock = models.PositiveIntegerField(default=0)
# 	adicional_stock = models.PositiveSmallIntegerField(default=0)
# 	descripcion = models.TextField(max_length=400)
# 	fecha_ingreso = models.DateTimeField(auto_now=True ,editable=False)
# 	class Meta:
# 		unique_together = ('producto_id',)

# 	def save(self):
# 		agregar = Utilidades().validarIngresoNum(self.adicional_stock)
# 		if agregar != 0 :
# 			stock_antes = self.stock
# 			self.stock += agregar
# 			self.adicional_stock = 0
# 			super(DetalleAlmacen, self).save()
# 			try:
# 				HistorialDetalleAlmacen.objects.create(
# 					adicional_producto = agregar,
# 					stock_actual = stock_antes,
# 					detalle_almacen_id = self
# 				)
# 			except Exception, e:
# 				print '%s' %(e)
# 		else:
# 			super(DetalleAlmacen, self).save()

# class EstadoSucursal(models.Model):
#     nombre_estado = models.CharField(max_length=60)
#     def clean(self):
#         self.nombre_estado = self.nombre_estado

#     def __str__(self):
#         return self.nombre_estado
#     class Meta:
#     	verbose_name_plural= "Registro de Estados de Sucursales"

class Sucursal(models.Model):
	id_almacen = models.ForeignKey(Almacen)
	codigo_puesto = models.CharField(max_length=20)
	nombre = models.CharField(max_length=60)
	fecha_registro = models.DateTimeField(auto_now=True,editable=False)
	todos_departamento = (('Ama','Amazonas'), ('Anc','Ancash'),('Apu','Apurimac'),('Are','Arequipa'),('Aya','Ayacucho'),('Caj','Cajamarca'),('Cal','Callao'),('Cuz','Cuzco'),('Hua','Huancavelica'),('Hun','Huanuco'),('Ica','Ica'),('Jun','Junin'),('Lal','La Libertad'),('Lam','Lambayeque'),('Lim','Lima'),('Lor','Loreto'),('Mad','Madre de Dios'),('Moq','Moquegua'),('Pas','Pasco'),('Piu','Piura'),('Pun','Puno'),('San','San Martin'),('Piu','Piura'),('Tac','Tacna'),('Tum','Tumbes'),('Uca','Ucayali'),)
	departamento = models.CharField(max_length=20, choices=todos_departamento, default='Lim')
	todos_nombre_estado = (('Dis', 'Disponible'),('Fue', 'Fuera de Servicio'),('Man', 'En Mantenimiento'),('Cer','Cerrado'),)
	nombre_estado = models.CharField(max_length=20, choices=todos_nombre_estado, default='Dis')
	direccion = models.CharField(max_length=80)
	telefono = models.CharField(max_length=20)
	celular = models.CharField(max_length=20)
	#id_estadoSucursal = models.ForeignKey(EstadoSucursal)
	descripcion = models.TextField(max_length=400)
	def clean(self):
		self.codigo_puesto = self.codigo_puesto.capitalize()
		self.nombre = self.nombre.capitalize()
		validate_only_one_instance(self, Constante.CANTIDAD_SUCURSAL_PBASCICO)
	class Meta:
		verbose_name_plural = "Mantenimiento de Sucursales"
		unique_together = ('codigo_puesto', 'departamento',)
	def __unicode__(self):
		return " %s de la ciudad: %s con el codigo: %s" %(self.nombre,self.departamento,self.codigo_puesto)
	def save(self):
		try:
			with transaction.atomic():
				estado = Sucursal.objects.get(pk=self.id)	
				estado = estado.get_nombre_estado_display()
				if estado != self.get_nombre_estado_display():
					HistorialSucursal.objects.create(estado_antes = estado  ,estado_actual= self.get_nombre_estado_display(),id_sucursal = self )
				super(Sucursal, self).save()
		except Exception, e:
			print 'Error Historial 1: %s' %(e)
			print '***********'
			try:
				with transaction.atomic():
					super(Sucursal, self).save()
					HistorialSucursal.objects.create(estado_antes = self.get_nombre_estado_display()  ,estado_actual= self.get_nombre_estado_display() ,id_sucursal = self )
			except Exception, e:
				print 'Error Historial 2: %s' %(e)
				print '****************************'

# class HistorialDetalleAlmacen(models.Model):
# 	adicional_producto = models.PositiveIntegerField()
# 	stock_actual = models.PositiveIntegerField()
# 	fecha_ingreso = models.DateTimeField(auto_now=True , editable=False)
# 	detalle_almacen_id = models.ForeignKey(DetalleAlmacen)
# 	#sucursal_id = models.ForeignKey(Sucursal, null=True)

class DetalleSucursalAlmacen(models.Model):
	stock = models.PositiveIntegerField(default=0)
	adicional_stock = models.PositiveSmallIntegerField(default=0)
	producto_id = models.ForeignKey(Producto)
	sucursal_id = models.ForeignKey(Sucursal)
	fecha_ingreso = models.DateTimeField(auto_now=True , editable=False)

	class Meta:
		unique_together = ('producto_id','sucursal_id')
	def __unicode__(self):
		return u'%s' % (self.producto_id)



#Se Registra cuando se cambia de estado la sucursal
class HistorialSucursal(models.Model):
	fecha = models.DateTimeField(auto_now=True)
	estado_antes = models.CharField(max_length = 60)
	estado_actual = models.CharField(max_length = 60)
	id_sucursal = models.ForeignKey(Sucursal)

class HistorialDetalleSucursalAlmacen(models.Model):
	stock_actual = models.PositiveIntegerField()
	stock_adicional = models.PositiveIntegerField(default=0)
	fecha_ingreso = models.DateTimeField(auto_now=True , editable=False)
	id_detalle_sucursal_almacen = models.ForeignKey(DetalleSucursalAlmacen)



class SucursalTrabajador(models.Model):
	dni = models.CharField(max_length=8, unique=True)
	trabajador = models.OneToOneField(User)
	sucursal = models.ForeignKey(Sucursal)
	fecha_ingreso = models.DateTimeField(auto_now=True, editable=False)
	todos_cargo= (("admi","Administrador"),("empl" ,"Empleado"),)
	todos_estado= (("act","Activo"),("ina" ,"Inactivo"),)
	estado_empleado = models.CharField(null=True,max_length='8',choices =todos_estado, default='act')
	cargo = models.CharField(max_length=20 , choices= todos_cargo ,  default="empl")
	fecha_nacimiento = models.DateField(blank=True , null=True,default=date(1990,01,01))
	sexo = models.CharField( max_length =1, choices= (("m","Masculino") , ("f","Femenino")) , default="m")
	def save(self):
		flag = True
		try:
			usuario =User.objects.get(pk=self.trabajador.id)
			print usuario.is_active
			print "ACTIVADOOOO"
			if self.cargo == 'admi':
				usuario.is_staff = True
			elif self.cargo == 'empl':
				usuario.is_staff = False
			else:
				flag = False
			if self.estado_empleado == 'act':
				usuario.is_active = True
			elif self.estado_empleado == 'ina':
				usuario.is_active = False
			else:
				flag = False
			if flag:
				usuario.save()
				print "LLEGA TRABAJADOR"
				super(SucursalTrabajador, self).save()
			else:
				print "mensaje de error"
		except Exception, e:
			print "Mensaje de error: %s" %(e)
	def __unicode__(self):
		return " Trabjador: %s , %s" %(self.trabajador,self.sucursal,)	

	class Meta:
		verbose_name_plural = "Trabajadores"	
#Modelo Cliente  , no deberia estar  aqui pero por el momento
class Cliente(models.Model):
	razon_social = models.CharField(max_length=50 , blank=True);
	nombre = models.CharField(max_length=50)
	apellidos = models.CharField(max_length=50)
	telefono = models.CharField(max_length=10)
	dni = models.CharField(unique=True, max_length = 8 ,validators=[ RegexValidator(regex = '\d{8}', message="DNI no tiene 8 digitos", code="invalido")])
	direccion = models.CharField(max_length=50 , blank=True)	
	ruc = models.CharField(max_length=11 , blank=True)
	correo = models.EmailField(blank=True)


	def __unicode__(self):
		return "Cliente : [%s] %s %s " %(self.razon_social,self.nombre , self.apellidos)






