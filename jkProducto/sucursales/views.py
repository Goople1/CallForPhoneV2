# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response , HttpResponse
from django.template.context import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.utils import timezone
from django.db.models import Q,Sum, F
from django.core.paginator import Paginator

import json
import djqscsv
import datetime

from .models import Sucursal, DetalleSucursalAlmacen, HistorialDetalleSucursalAlmacen,HistorialSucursal
from almacen.models import DetalleAlmacen
from productos.models import Producto
from sucursales.utilidades import Utilidades
from ventas.models import Venta
from ventas.models import DetalleVenta






# Create your views here.

@login_required(login_url='/cuenta/')
def mantenimientoSucursal(request):
	#template = 'MantenimientoAsignacionSucursales.html'
	#template = 'modificarProductoSucursalOriginal.html'
	#template = 'ListarProductosOriginal.html'
	# template = 'signin.html'
	#template = "IndiceOriginal.html"
	#template = 'AddProductosSucursal.html'
	#template = 'ListarSucursales.html' #fake
	#template = 'registrarProductoOriginal.html'

	if  is_admin(request.user.id):
		template = 'mantenimientoSucursal.html'
		datos = request.session["datos"]
		return render_to_response(template,{"datos":datos},context_instance = RequestContext(request))
	else :
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def addSucursal(request):
	if is_admin(request.user.id):
		template='ListarSucursales.html'
		template = "IndiceOriginal.html"
		operation = 'addSucursalA'
		estado ="Registrar"
		sucursal = Sucursal.objects.all()
		datos = request.session["datos"]

		return render_to_response(template,{'sucursales':sucursal,'estado':estado,'operation':operation , "datos":datos},context_instance=RequestContext(request))

	else :
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def editSucursal(request):
	if is_admin(request.user.id):
		template='ListarSucursales.html'
		template = "IndiceOriginal.html"
		operation = 'editSucursalE'
		estado = "Modificar"
		sucursal = Sucursal.objects.all()
		datos = request.session["datos"]

		return render_to_response(template,{'sucursales':sucursal, 'estado':estado,'operation':operation,"datos":datos},context_instance=RequestContext(request))

	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def listSucursal(request):
	if is_admin(request.user.id):
		template='ListarSucursales.html'
		template = "IndiceOriginal.html"
		operation = 'listSucursalL'
		estado = "Listar"
		sucursal = Sucursal.objects.all()
		datos = request.session["datos"]

		return render_to_response(template,{'sucursales':sucursal, 'estado':estado,'operation':operation , "datos" : datos},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def historialVentas(request):
	if is_admin(request.user.id):
		template = "IndiceOriginal.html"
		operation = 'histoSucursalVentasAdm'
		sucursal = Sucursal.objects.all()
		datos = request.session["datos"]
		estado = "Historial"
		return render_to_response(template,{'sucursales':sucursal,'estado':estado,'operation':operation , "datos":datos},context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def Historial_ventas_Sucursal_Admin(request,id):

	if is_admin(request.user.id):

		sucursal_id = Utilidades().validarIngresoNum(id)

		try:
			ventas  = Venta.objects.filter(sucursal = sucursal_id).order_by('-fecha_emision')
			
		except Exception,e :
			print e

		template  = "reporteHistorialVenta.html"
		datos = request.session["datos"]
		return render_to_response(template , {"ventas":ventas , "datos" : datos} , context_instance  = RequestContext(request))

	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def historialSucursal(request):

	if is_admin(request.user.id):
		historialSucursal = []
		try:
			
			historialSucursal  = HistorialSucursal.objects.all().order_by('-fecha')
		except Exception,e :
			print e

		template  = "reporteHistorialSucursal.html"
		datos = request.session["datos"]
		return render_to_response(template , {"historialSucursal":historialSucursal , "datos" : datos} , context_instance  = RequestContext(request))

	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def addSucursalA(request,id):

	#template = 'AddProductosSucursal.html'
	#template = 'mantenimientoSucursal.html'

	if is_admin(request.user.id):

		template = 'registrarProductoOriginal.html'

		#para Sacar los productos  que ya existen en  los DetallesSucursalAlmacen  de una Sucursal
		sucursal_id = id

		try:
			Sucursal.objects.get(pk=sucursal_id)
			try:
				detalle_sucursal_almacen_productos = DetalleSucursalAlmacen.objects.filter(sucursal_id = sucursal_id)
			
			except Exception, e:
				print e
				return  HttpResponse("PROBLEMAS CON SERVER")
			

			if detalle_sucursal_almacen_productos:
				id_producto_detalle_sucu_almacen = [deta.producto_id for deta in  detalle_sucursal_almacen_productos]
				#print "Productos en Detalle Sucursal Almacen"
				#print id_producto_detalle_sucu_almacen
				#print "Productos En Detalle Almacen que no estan En DetalleSucursalAlmacen "
				detalle_almacen_productos = DetalleAlmacen.objects.exclude(producto_id__in= id_producto_detalle_sucu_almacen)
				#print detalle_almacen_productos


			else:
				#print " No hay nada en la lista asi que rojo par y pasa "
				detalle_almacen_productos  =  DetalleAlmacen.objects.only("producto_id")
		
		except Exception, e:
			return HttpResponse("<html><body>PAGE NOT FOUND</body></html>")

		datos = request.session["datos"]
		return render_to_response (template, {'productos':detalle_almacen_productos ,'id_sucursal': sucursal_id , "datos":datos} , context_instance = RequestContext(request))

	else :
		return HttpResponseRedirect("/ventas/")

		
@login_required(login_url='/cuenta/')
def editSucursalE(request,id):
	if is_admin(request.user.id):
		#template  = "modificarProductoSucursal.html"
		template = "modificarProductoSucursalOriginal.html"
		sucursal_id = id
		
		
		try:

			Sucursal.objects.get(pk=sucursal_id)
			
			try:
				detalle_sucursal_almacen_productos = DetalleSucursalAlmacen.objects.filter(sucursal_id = sucursal_id)
			except Exception, e:
				print e
				return HttpResponse("Problemas Con el  Server")

		except ObjectDoesNotExist,e:

			return HttpResponse("<html><body>PAGE NOT FOUND</body></html>")

		id_producto_detalle_sucu_almacen = [detalle.producto_id for detalle  in detalle_sucursal_almacen_productos]

		datos = request.session["datos"]

		return render_to_response(template,{"productos": id_producto_detalle_sucu_almacen , 'id_sucursal': sucursal_id , "datos":datos },context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect("/ventas/")
	



@login_required(login_url='/cuenta/')
def listSucursalL(request,id , page = 1):
	#verificar si el user que ha ingresado es admin , de lo contrario , seria un vendedor :D
	if is_admin(request.user.id):

		#verificar que el  parametro que se obtiene por  la URL , sea un numero
		sucursal_id = Utilidades().validarIngresoNum(id)
		try:

			#obtener  la sucursal media el id que se brinda
			sucursal = Sucursal.objects.get(pk=sucursal_id)

			try:

				#Aca se obtiene TODOS los productos que han sido ASIGNADOS a la SUCURSAL , tener en cuenta que los productos Existentes son Sacados del ALMACEN
				#A RODAR

				#1.-  obtener la cantidad de productos en la Sucursal ....
				detalle_sucursal_almacen_productos = DetalleSucursalAlmacen.objects.filter(sucursal_id = sucursal)
				#2.-  designar la cantidad productos tiene que haber por pagina ... por el momento para esta fase de desarrollo probare con 4 por pagina , lo conversado con MSJ es 10 aprox hasta 15 max
				page = request.GET.get('page' , 1)

				print "PAGAE:" , page

				pagination = Paginator(detalle_sucursal_almacen_productos, 4)

				#3.-  SABER en que numero de Pagina se esta actualmente

				try:
					producto_x_page = pagination.page(page)
    			
				except PageNotAnInteger:
					producto_x_page = paginator.page(1)

    			except EmptyPage:
        			producto_x_page = paginator.page(pagination.num_pages)


				#4.-  SABER si tiene Pagina anterior
				#5.-  SABER si TIENE pagina Siguiente
				#6.-  Si es la ultima pagina

			except Exception, e:
				return HttpResponse("Problemas del Server")

		
		except Exception, e :
			print e
			mensaje ="<html>	<head>		<title></title>		</head>		<body>			<h1> PAGE NOT FOUND!</h1>		</body>		</html>"
			return HttpResponse(mensaje)
		#template = "listaProductosSucursalAlmacen.html"
		template = "ListarProductosOriginal.html"
		datos = request.session["datos"]

		return render_to_response (template, {'producto_x_page':producto_x_page , 'sucursal':sucursal , 'datos':datos} , context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect("/ventas/")

@login_required(login_url='/cuenta/')
def listPages(request):
	page = request.GET.get('page')
	pass
	
#Asignacion de Pedidos a Sucursales
def registrarPedidoSucursal(request):
	pass

@login_required(login_url='/cuenta/')
def dameStock(request):


	if request.method == "GET":
		#print "pase el get"
		a =  request.GET.get("codigo_producto")

		codigo_producto = Utilidades().validarIngresoNum(a)
		#print codigo_producto

		if(codigo_producto != 0) & (codigo_producto > 0):
			try:
				
				da = DetalleAlmacen.objects.get(producto_id=codigo_producto)
			except Exception, e:

				print e
				return HttpResponse("Problemas Con el SERVER!!!")
			
			da = da.stock
			return  HttpResponse(da)

		else:
			mensaje = "imposible de encontrar el Producto "
			return HttpResponse(mensaje)
	else :
		return HttpResponse("Only Get")


@login_required(login_url='/cuenta/')
def addProductotoSucursal(request):

	if request.method == "POST":
		producto_id = Utilidades().validarIngresoNum(request.POST.get("producto_id"))
		sucursal_id  = Utilidades().validarIngresoNum(request.POST.get("sucursal_id"))
		stock_add = Utilidades().validarIngresoNum(request.POST.get("stock_add"))
		if ((producto_id != 0) & (producto_id > 0) ):

			#print "pass"
			if stock_add > 0 :

				#print "pase is digit"
				try :
					detalle_almacen = DetalleAlmacen.objects.get(producto_id = producto_id )
				except Exception,e:
					print e
					mensaje = "Problemas con el SERVER"
					return HttpResponse(mensaje)

				#print detalle_almacen
				detalle_almacen.stock -= stock_add
				

				try:
					producto = Producto.objects.get(id = producto_id)
				except ObjectDoesNotExist, e :
					print e
					mensaje = "Producto no Encontrado,Pruebe otra vez"
					return HttpResponse(mensaje)
				
				try :
					sucursal = Sucursal.objects.get(id = sucursal_id)
				except ObjectDoesNotExist, e:
					print e
					mensaje = "Es posible que la Sucursal no Exista, Intente otra vez"
					return HttpResponse(mensaje)

				#print producto
				#print "............"
				#print sucursal
				#print "Creando el detalleSurcusalAlmacen"
				# Para crear Objetos con  campos que son llaves Foraneas ,  se debe Vincular  un  Objeto  del Tipo  de  esa  Llave
				#print "fin de Crear detalleSurcusalAlmacen"
				#se Crea el DetalleSucursalAlamcen

				try:
					detalleSA = DetalleSucursalAlmacen(stock = stock_add, producto_id = producto , sucursal_id =  sucursal)
					
					detalleSA.save()
					HistorialDetalleSucursalAlmacen.objects.create(stock_actual =detalleSA.stock ,id_detalle_sucursal_almacen=detalleSA)

				except Exception , e :
					print e
					mensaje = "no se puede Guardar los Datos , Parece Que ya Existen , Intente Otro vez"
					return HttpResponse(mensaje)

				detalle_almacen.save()
				return HttpResponse("Done!")
				#SeGuardan Los cambios para el Stock de DetalleAlmacen

			else:
				return HttpResponse("Algo va mal ")
		else :
			return HttpResponse("No se Eligio ningun Producto")

	else:
		return HttpResponse("No es posible esta accion por metodo Get")

@login_required(login_url='/cuenta/')
def StockDetalleSucursalAlmacen(request):

	
	if request.method == "GET":

		cod_prod = Utilidades().validarIngresoNum(request.GET.get('codigo_producto'))
		cod_suc = Utilidades().validarIngresoNum(request.GET.get('codigo_sucursal'))

		

		if (cod_prod != 0) & (cod_prod > 0) :
			try:
				product = DetalleSucursalAlmacen.objects.get(sucursal_id = cod_suc,producto_id = cod_prod)

			except Exception, e:
				print e
				return HttpResponse("Problemas con el Server!!!!")
			
			rsp =  product.stock
			return HttpResponse(rsp)
			
		else:
			mensaje = "No se Eligio ningun producto"
			print mensaje
			mensaje = ""
			return HttpResponse(mensaje)


	else:
		mensaje = "27 rojo , impar  y pasas "
		print mensaje
		return HttpResponse(mensaje)


@login_required(login_url='/cuenta/')
def editProductotoSucursal(request):

	if request.method == "POST":
		
		sucursal_id  = Utilidades().validarIngresoNum(request.POST.get("sucursal_id",0))

		producto_id = Utilidades().validarIngresoNum(request.POST.get("producto_id",0))
		#funcion que cuando no sea un numero me retorne 0
		stock_add = Utilidades().validarIngresoNum(request.POST.get("stock_add",0))
		# stock_dispo = request.POST.get("stock_dispo")


		if(producto_id != 0 )& (producto_id > 0):

			if (stock_add !=0) & (producto_id > 0):


				try:
					producto_detalle_sucursal_almacen = DetalleSucursalAlmacen.objects.get(sucursal_id=sucursal_id , producto_id=producto_id)
				except Exception,e :
					print e
					return HttpResponse("No Es Posible Editar  el Producto  en  la Sucursal ")

				print producto_detalle_sucursal_almacen.producto_id
				print producto_detalle_sucursal_almacen.stock

				try:
					detalle_almacen = DetalleAlmacen.objects.get(producto_id=producto_id)
				except Exception, e:
					print e
					return HttpResponse ("Problemas con el Server")

				if(detalle_almacen.stock >= stock_add):
					detalle_almacen.stock-=stock_add
					antes_dsa = producto_detalle_sucursal_almacen.stock
					producto_detalle_sucursal_almacen.stock+=stock_add
					detalle_almacen.save()
					producto_detalle_sucursal_almacen.save()
					HistorialDetalleSucursalAlmacen.objects.create(stock_actual =antes_dsa,stock_adicional= stock_add,id_detalle_sucursal_almacen=producto_detalle_sucursal_almacen)
					return HttpResponse("Modificacion  del Producto hecha")
				else:
					mensaje = "La Cantidad En el Almacen  no es Suficiente para su Pedido"
					print mensaje
					return HttpResponse(mensaje)
			else:

				mensaje = "no se Puede Agregar esta cantidad  , Cambiela porfavor"
				return HttpResponse(mensaje)

		else:
			mensaje = "Imposible encontrar el producto"
			print mensaje
			return HttpResponse(mensaje)

	else:
		return HttpResponse(" Problemas Con el Server")






def is_admin(user_id):

	user = User.objects.get(id = user_id)

	if user.is_staff:

 		return True

	else:
		return False

def export(request , suc_id):
	sucursal_id = Utilidades().validarIngresoNum(suc_id)

	detalle_productos_sucursal	=	DetalleSucursalAlmacen.objects.filter(sucursal_id = sucursal_id)

	data = detalle_productos_sucursal.values('id','producto_id__tipo_producto__nombre','producto_id__marca__nombre','producto_id__codigo','producto_id__color','stock','producto_id__precio_x_menor','producto_id__precio_x_mayor')	
	#field_header_map={'producto_id__tipo_producto__nombre': 'TIPO','producto_id__marca__nombre':'MARCA','producto_id__codigo': 'MODELO' , 'producto_id__color':'COLOR', 'producto_id__precio_x_menor': 'PRECIO por Menor' , 'producto_id__precio_x_mayor': 'Precio por Mayor'}
	
	# qs = Producto.objects.all()
	return djqscsv.render_to_csv_response(data,field_header_map = {'producto_id__tipo_producto__nombre': 'TIPO','producto_id__marca__nombre':'MARCA','producto_id__codigo': 'MODELO' , 'producto_id__color':'COLOR', 'producto_id__precio_x_menor': 'PRECIO por Menor' , 'producto_id__precio_x_mayor': 'Precio por Mayor'})


@login_required(login_url='/cuenta/')
def ver_detalle(request):
	

	if request.method == "GET":


		if request.user.is_staff:


			codido =Utilidades().validarIngresoNum(request.GET.get("codigo"))
			try:
				venta = Venta.objects.get(id = codido)
			except Exception, e:
				print e
				HttpResponse("Error")
			det = DetalleVenta.objects.filter(venta_id = venta.id)

			if det:
				data = [Utilidades().detalle_venta_to_json(detalle) for detalle in det]


			else :
				data = []
			return HttpResponse( json.dumps(data) , content_type='application/json')

		else :
			return HttpResponse("Zorry")


	else :
		return HttpResponse("Zorry")





@login_required(login_url='/cuenta/')
def getVentasbyDateRange(request):
	if request.method == 'GET':
		sum_ventas = {}
		fecha_inicio = request.GET.get("fechaInicio","")
		fecha_fin = request.GET.get("fechaFinal","")
		if fecha_inicio.strip() !="":
			fecha_inicio = map(int ,request.GET.get("fechaInicio").split("/"))
		#	print fecha_inicio
			fecha_inicio = timezone.make_aware(datetime.datetime(day = int(fecha_inicio[0]) , month = int(fecha_inicio[1]) , year = int(fecha_inicio[2])))
		
		if fecha_fin.strip() != "":
			fecha_fin = request.GET.get("fechaFinal").split("/")
			fecha_fin = timezone.make_aware(datetime.datetime(day = int(fecha_fin[0]) , month = int(fecha_fin[1]) , year = int(fecha_fin[2]) , hour =23  , minute  = 59 , second = 50 ))

		#print fecha_inicio , " --- " , fecha_fin
		rpt = criteriobusqueda(fecha_inicio,fecha_fin)
		 # buscar todas la ventas en ese rango de fechas :
		#ventas_date_range = Venta.objects.filter(fecha_emision__range=(fecha_inicio, fecha_fin))
		try:
			#ventas_date_range = Venta.objects.filter(Q(fecha_emision__gte=(datetime.date(day = fecha_inicio[0] , month = fecha_inicio[1] , year = fecha_inicio[2]))), Q(estado = True))

			#ventas_date_range = Venta.objects.filter(Q(fecha_emision__gte=fecha_inicio) ,Q(fecha_emision__lte = fecha_fin),  Q(estado = True))
			ventas_date_range = Venta.objects.filter(**rpt)
			total = Venta.objects.all()
		#	print total[0].fecha_emision
		#	print ventas_date_range[0].fecha_emision
			# total_ventas = Venta.objects.annotate(total_venta = Sum('total'))
			# print "total" ,  total_ventas
			sum_ventas  = ventas_date_range.aggregate(total  =  Sum(F('total')))

			print sum_ventas
		except Exception, e:			
			print e
		#print "test 123"
		venta_json_format = [Utilidades().venta_to_json(venta) for venta in ventas_date_range]
		#print venta_json_format
		venta_json_format.append(sum_ventas)
		#venta_json_format.update(sum_ventas)
		#print venta_json_format
		return HttpResponse( json.dumps(venta_json_format) , content_type='application/json')


def criteriobusqueda(fecIni,fecFin):

	criterio = {}
	regla = {'estado': True }
	criterio.update(regla)
	#any() retorna   True si alguna condicion es True
	
	valor = [fecIni,fecFin]
	if  not any(valor) :
		# try:
		# 	todo = DetalleSucursalAlmacen.objects.all()
		# except Exception,e:
		# 	print e
		# 	return HttpResponse("Servidor OFf")
		return criterio
	else:

		campos = ["fecIni","fecFin"]
		my_dict = dict(zip(campos,valor))
		my_dict = clean_dict_for_value_0(my_dict)

		if "fecIni" in my_dict :
			regla = {"fecha_emision__gte":my_dict.get("fecIni")}
			criterio.update(regla)

		if "fecFin" in my_dict:
			regla = {"fecha_emision__lte":my_dict.get("fecFin")}
			criterio.update(regla)

		return criterio

#funcion para limpiar  un dictionario  con value difrente de 0
#Teniendo en cuenta que los valores que se pasan son 0 o positivos
def clean_dict_for_value_0 (data):

	d = {k:v for k, v in list(data.items()) if v }

	return d


@login_required(login_url='/cuenta/')
def getGananciabyDateRange(request):

	#print "LA GANACIA ES.............."
	if request.method == 'GET':

		fecha_inicio = map(int ,request.GET.get("fechaInicio").split("/"))
		fecha_inicio = timezone.make_aware(datetime.datetime(day = int(fecha_inicio[0]) , month = int(fecha_inicio[1]) , year = int(fecha_inicio[2])))
		
		fecha_fin = request.GET.get("fechaFinal").split("/")
		fecha_fin = timezone.make_aware(datetime.datetime(day = int(fecha_fin[0]) , month = int(fecha_fin[1]) , year = int(fecha_fin[2]) , hour =23  , minute  = 59 , second = 59 ))

		try:
			ventas = Venta.objects.filter(Q(fecha_emision__gte=fecha_inicio) ,Q(fecha_emision__lte = fecha_fin),  Q(estado = True))
			sum_ventas  = ventas.aggregate(suma_totales_venta  =  Sum(F('total')))

	#		print sum_ventas

		except Exception, e:
			print e

		return HttpResponse( json.dumps(sum_ventas) , content_type='application/json')
		


class invitePage (TemplateView):
	template_name = 'invitar.html'






# def sessionData(request):
#     if request.session['datos']:
#         return request.session['datos']
#     else:
#         try:
#             trabajador = SucursalTrabajador.objects.get(trabajador = request.user)
#             if trabajador.cargo.lower() == "empl":
#                 request.session["datos"] = {"empresa": trabajador.sucursal.nombre,"nombre":trabajador.trabajador.get_full_name()}
#             else :
#                 if trabajador.cargo.lower() == "admi":
#                     request.session["datos"] = {"empresa": trabajador.sucursal.id_almacen.nombre_empresa,"nombre":trabajador.trabajador.get_full_name()}
#         except Exception ,e :
#             if acceso.is_staff:
#                 request.session['datos'] = {"empresa": "Administrador","nombre":request.user.get_full_name()}
#             return request.session['datos']








