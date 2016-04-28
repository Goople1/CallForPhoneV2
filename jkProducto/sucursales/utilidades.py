# -*- coding: utf-8 -*-
# from django.db.models import ForeignKey 
from django.utils import timezone
import locale
#import datetime
locale.setlocale(locale.LC_TIME,'')
#'es_CR.UTF-8'
class Utilidades():
	def validarIngresoNum(self,numero):

		if numero != None :
			numero = str(numero) if str(numero).isdigit()  else numero.strip()
			if numero.isdigit():
				numero=int(numero)
				if numero > 0 :
					return numero
				else:
					return 0
			else :
				return 0
		return 0




	# def mifuncion(self,model_instance):
	# 	json = {}
	# 	for field in model_instance._meta.get_all_field_names():
	# 		print field
	# 	 	field_object, model, direct, m2m = model_instance._meta.get_field_by_name(field)
 #    		if not m2m and direct and isinstance(field_object, ForeignKey):
    			
 #    			print "es llave Foranea"
 #    		else:
 #    			json[field] = model_instance.__getattribute__(field)

			
	#     return json


	def detalle_sucursal_almacen_to_json (self,ObjDetaSucAlm):
		to_json = {	"id" : ObjDetaSucAlm.id,"stock" : ObjDetaSucAlm.stock, "producto": {"id" : ObjDetaSucAlm.producto_id.id,"codigo":ObjDetaSucAlm.producto_id.codigo,"color" :ObjDetaSucAlm.producto_id.get_color_display(),"precio_por_mayor":str(ObjDetaSucAlm.producto_id.precio_x_mayor),"precio_por_menor":str(ObjDetaSucAlm.producto_id.precio_x_menor),"imagen":ObjDetaSucAlm.producto_id.imagen.url,	"marca":{"nombre":ObjDetaSucAlm.producto_id.marca.nombre},  "tipo_producto":{"nombre":ObjDetaSucAlm.producto_id.tipo_producto.nombre}   }, 	"sucursal":{"codigo_puesto":ObjDetaSucAlm.sucursal_id.codigo_puesto, "nombre":ObjDetaSucAlm.sucursal_id.nombre,	"departamento":ObjDetaSucAlm.sucursal_id.get_departamento_display(),"direccion":ObjDetaSucAlm.sucursal_id.direccion, "telefono":ObjDetaSucAlm.sucursal_id.telefono, "celular":ObjDetaSucAlm.sucursal_id.celular }}
		return to_json



	def venta_to_json(self,ObjVenta):
		print "venta"
		#print strftime("%a, %d %b %Y %H:%M:%S")
		to_json = {"id": ObjVenta.id , "empleado" : str(ObjVenta.empleado.trabajador.get_full_name()) , "sucursal": str(ObjVenta.sucursal.nombre), "fecha_emision" : str(timezone.localtime(ObjVenta.fecha_emision).strftime("%a, %d %b %Y %I:%M %p")).capitalize() , "total": ObjVenta.total , "tipo":ObjVenta.get_nombre_ventas_descripcion_display()	}
		return to_json


	def detalle_venta_to_json(self,ObjDetalleVenta):

		to_json = {"producto":str(ObjDetalleVenta.detalle_Sucursal_almacen_id.producto_id), "tipo_precio" : ObjDetalleVenta.tipo_precio ,"cantidad" :ObjDetalleVenta.cantidad , "precio":ObjDetalleVenta.precio , "descripcion" : ObjDetalleVenta.descripcion ,"importe": ObjDetalleVenta.importe , "precio_real":ObjDetalleVenta.precio_real}
		return to_json

	def cliente_to_json(self,ObjCli):
		print "cliente"
		#print strftime("%a, %d %b %Y %H:%M:%S")
		to_json = {"id": ObjCli.id , "razon_social_nombre" : str(ObjCli.razon_social_nombre) , "telefono": str(ObjCli.telefono), "ruc_dni" : str(ObjCli.ruc_dni) , "correo": (ObjCli.correo) , "tipo_cliente":ObjCli.tipo_cliente	}
		return to_json































# from django.contrib.auth.models import User
# class ValidarUsuario():



    	# "id" : ObjDetaSucAlm.id,
    	# "stock" : ObjDetaSucAlm.stock,
    	# "producto": {
    	# 				"id" : ObjDetaSucAlm.producto_id.id,
    	# 				"codigo":ObjDetaSucAlm.producto_id.codigo,
    	# 				"color" :ObjDetaSucAlm.producto_id.color,
    	# 				"precio_por_mayor":ObjDetaSucAlm.producto_id.precio_x_mayor
    	# 				"precio_por_menor":ObjDetaSucAlm.producto_id.precio_x_menor

    	# 				"marca":{
    	# 					"nombre":ObjDetaSucAlm.producto_id.marca.nombre

    	# 				}

    	# 				"tipo_producto":{

    	# 					"nombre":ObjDetaSucAlm.producto_id.tipo_producto.nombre
    	# 				}


    	# 			}

     #   	"sucursal":{

     #   			"codigo_puesto":ObjDetaSucAlm.sucursal_id.codigo_puesto,
     #   			"nombre":ObjDetaSucAlm.sucursal_id.nombre,
     #   			"departamento":ObjDetaSucAlm.sucursal_id.departamento,
     #   			"direccion":ObjDetaSucAlm.sucursal_id.direccion,
     #   			"telefono":ObjDetaSucAlm.sucursal_id.telefono,
     #   			"celular":ObjDetaSucAlm.sucursal_id.celular

     #   		}


#     def validarEmail(self,dato):
#         rpta={}
#         print dato
#         if '@' in dato:
#             us=User.objects.filter(email__iexact=dato)
#             #1-> Si existe - 0->No existe
#             rpta['valido'] = "1" if us else "0"
#             #print valor
            
#             #Consultar
#         else:
#             #3->Email Invalido - 4->Cadena Vacio
#             rpta['valido'] = "3" if len(dato)!=0 else "4"
#         return rpta
#            # if dato.length==0:
#             #    print "No hay data"
#            # print "Este email no es valido"

#     def validarNombre(self,dato):
#         rpta={}
#         #0->Si  dato, tiene elementos
#         #4->Si dato, es vacia 
#         rpta['valido'] = "0" if len(dato)!=0 else "4"
#         return rpta

#     def validarPassword(self,dato):
#         rpta={}
#         #0->Si  dato,tiene 6 o mas caracteres.
#         #4->Si dato, tiene 5 o menos caracteres. 
#         rpta['valido'] = "0" if len(dato)>=6 else "4"
#         return rpta

#     def validarUsername(self,dato):
#         rpta={}
#         if len(dato) < 1:
#             #4-> Si dato, es vacio
#             rpta['valido'] = "4"
#         else:
#             us=User.objects.filter(username__iexact=dato)
#             print us
#             #1->Si existe ese username
#             #0->No existe, es libre.
#             rpta['valido'] = "1" if us else "0"

#         return rpta

#     def validarTodos(self,nombre='',email='',password='',username=''):
#         return {'validoN': self.validarNombre(nombre).get('valido',''),
#         'validoE': self.validarEmail(email).get('valido',''),
#         'validoP': self.validarPassword(password).get('valido',''),
#         'validoU': self.validarUsername(username).get('valido','')}
#         #,self.validarEmail(email),self.validarPassword(password),self.validarUsername(username)}

#     def passwordZero(self,password=''):
#         if len(password)> 5:
#             return True
#         return False

#     def passwordFirst(self, password=''):
#         if len(password)> 5:
#             return True
#         return False

#     def passwordSecond(self, password1, password2):
#         if len(password2) <6 :
#             return False
#         elif password1 == password2:
#             return True
#         else:
#             return False
