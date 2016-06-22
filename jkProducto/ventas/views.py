from django.shortcuts import render_to_response , HttpResponse
from django.template.context import RequestContext
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,logout
from django.core.urlresolvers import reverse


import datetime
import json

from sucursales.models import SucursalTrabajador,DetalleSucursalAlmacen
#,Sucursal
from sucursales.utilidades import Utilidades
from .models import  Venta , DetalleVenta
from cliente.models import Cliente
from .forms import FormInciarSesion
from cliente.forms import ClienteForm
from asistencia.models import AsistenciaTrabajador
#from almacen.models import Almacen
#from productos.models import Producto
# from django.http import HttpResponse
# Create your views here.
#fdef para el Home_empleado
#from django.utils import timezone

@login_required(login_url='/login/')
def home_ventas(request):
    print request.user.id
    #user_id =
    print request.user.id
    # try :
    #     trabajador = SucursalTrabajador.objects.get(trabajador = user_id)
    # except Exception , e :
    #     print e
    #     user = User.objects.get(id = user_id)
    #     print user
    #     if user.is_staff:
    #        return HttpResponseRedirect("/admin/")
    #         #return HttpResponse("Es  Usuario , Pero no Trabajador")
    # #template = "empleado_home.html"
    template = "homeEmpleado.html"
    datos = request.session["datos"]

    if  datos.get("cargo") == "empl":
        return render_to_response(template , {'datos':datos} ,context_instance=RequestContext(request))
    else :
        if datos.get("cargo") == "admi":
            print "soy admin"
            return HttpResponseRedirect("/admin/")



    #return render_to_response(template , {"trabajador": trabajador , 'datos':datos} ,context_instance=RequestContext(request))



@login_required(login_url='/login/')
def lista_producto(request):


    datos = request.session["datos"]

    if  datos.get("cargo") == "empl":
        trabajador = SucursalTrabajador.objects.get(trabajador=request.user.id)

        lista_producto = DetalleSucursalAlmacen.objects.filter(sucursal_id = trabajador.sucursal.id)
        template = "homeListaProductoSucursal.html"
        return render_to_response(template,{"detalle_sucursal_almacen_productos":lista_producto ,  "datos":datos} , context_instance = RequestContext(request))
    else :
        if datos.get("cargo") == "admi":
            return HttpResponseRedirect("/admin/")




@login_required(login_url='/login/')
def venta (request):	
    if request.method == "GET":

        datos = request.session["datos"]

        if  datos.get("cargo") == "empl":

            try:
                trabajador = SucursalTrabajador.objects.get(trabajador=request.user.id)
            except Exception , e :
                print e
                return HttpResponse("Error de BD :/")

            trabajador_sucursal_id = trabajador.sucursal.id
            lista_productos = DetalleSucursalAlmacen.objects.filter(sucursal_id = trabajador_sucursal_id)
            template = "homeVentas.html"
            #template = 'imprimir.html'
            registrar_cliente = ClienteForm(request.POST)
            venta  = True
            return  render_to_response( template , {"venta":venta,"productos": lista_productos, "trabajador":trabajador, "datos":datos,'registrar_cliente': registrar_cliente} , context_instance = RequestContext(request))

        else :
            if datos.get("cargo") == "admi":
                return HttpResponseRedirect("/admin/")


#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------

@login_required(login_url='/login/')
@transaction.atomic()
def addVenta(request):
    if request.method == "POST":
        print "resolviendo bug"
        estado_venta = False
        id_venta = 0
        respuesta = ''
        try:
            with transaction.atomic():
                #estado_venta = True
                trabajador = SucursalTrabajador.objects.get(trabajador = request.user.id)
                my_json_products_to_dict = json.loads(request.POST.get("json_detalle_venta"))
                total = Utilidades().validarIngresoNum(request.POST.get("total"))
                print "POST"
                print request.session.get("venta_id_to_modificar",False)
                if (bool(request.session.get("venta_id_to_modificar",False)) & bool(request.session.get("detalle_venta_dict_producto",False))):
                    print "IF"
                    venta_to_modificar = request.session.get("venta_id_to_modificar")
                    detalle_venta_load_products = request.session.get("detalle_venta_dict_producto")
                    venta = Venta.objects.get(id = venta_to_modificar)
                    venta.estado = False
                    venta.nombre_ventas_descripcion = 'ELI'
                    venta.save()
                    #cargar productos_to_load
                    if detalle_venta_load_products:
                        for producto in detalle_venta_load_products:
                            cantidad =  Utilidades().validarIngresoNum(producto.get("cantidad"))
                            producto_id = producto.get("producto_id")
                            det_sucu_alm_prod_to_add = DetalleSucursalAlmacen.objects.get(producto_id = producto_id , sucursal_id = venta.sucursal)
                            det_sucu_alm_prod_to_add.stock += cantidad
                            det_sucu_alm_prod_to_add.save()

                        if my_json_products_to_dict:
                            #eliminar sessiones creadas, cuando todo sale bien
                            del request.session['venta_id_to_modificar']
                            del request.session['detalle_venta_dict_producto']
                            id_venta, respuesta, flag = crearVenta(trabajador, total, my_json_products_to_dict,venta.cliente ,estado="MOD", referencia=venta_to_modificar)
                        else :
                            respuesta = "No se ha Podido Modificar esta Venta , intentelo luego"                      
                else:
                    print "ELSE"
                    mensaje = True
                    #validar la opc elegida
                    #opcion 1 - Anonimo
                    #opcion 2 - buscar
                    #opcion 3 - registrar Nuevo
                    radioVenta = request.POST.get("radioTipoVenta","")
                    if radioVenta == "2":
                        ##buscar cliente
                        try:
                            clienteNuevo = Cliente.objects.get(id = request.POST.get("hdnCliente", ""))
                        except Exception, e:
                            mensaje = False
                    elif radioVenta == "3":                
                        #registar cliente
                        print request.POST.get('clienteNuevoR')
                        dict_cliente = json.loads(request.POST.get('clienteNuevoR',{}))
                        txtRUC = dict_cliente.get('txtRucDni','')
                        txtRazon = dict_cliente.get('txtRazonNombre','')
                        cmbTipoCliente = dict_cliente.get('cmbTipoCliente','')
                        txtDireccion = dict_cliente.get('txtDireccion','')
                        txtCorreo = dict_cliente.get('txtCorreo','')
                        if txtRUC != '' and txtRazon != '' and cmbTipoCliente != '' and txtCorreo !='':
                            try:
                                clienteNuevo = Cliente.objects.create(ruc_dni=txtRUC, razon_social_nombre= txtRazon, tipo_cliente= cmbTipoCliente, correo= txtCorreo, direccion= txtDireccion )
                            except Exception, e:
                                print "error registrar cliente"
                                print e
                                mensaje = False
                    if mensaje:
                        if my_json_products_to_dict:
                            if radioVenta in ('2','3'):
                                id_venta, respuesta, flag = crearVenta(trabajador, total, my_json_products_to_dict,clienteNuevo)
                                print " ###slr"
                                print id_venta,respuesta
                            else:
                                id_venta, respuesta, flag = crearVenta(trabajador, total, my_json_products_to_dict) 


                                print "Else Print Anonimo"
                                print id_venta, respuesta 

                        else :
                            respuesta = "Json Vacio"
                    else:
                        respuesta = "Ha ocurrido un error"


        except Exception, e:
            print e
            estado_venta = False
            respuesta = "no se Pudo Agregar la venta , intentelo nuevamente"
            transaction.rollback()
            
        else:
            estado_venta = True
            transaction.commit()
           
        finally:
            
            if estado_venta and flag:
                try:
                    redirect = reverse('imprimirVenta',kwargs={'venta_id':id_venta})
                except Exception, e:
                    print e
            else:
                redirect = "#"

            rpt = { "mensaje": respuesta , "redirect": redirect }
            print rpt
            return HttpResponse(json.dumps(rpt) , content_type='application/json')



def crearVenta(trabajador,total,list_products,clienteNuevo = None,estado='NUE',referencia=None) :
    try:
        mensaje = ""
        flag = True
        with transaction.atomic():
            print ">>>>>Estado , Referencia" , estado , referencia
            venta = Venta(empleado = trabajador , sucursal = trabajador.sucursal , total = total, nombre_ventas_descripcion = estado , referencia = referencia, cliente = clienteNuevo)
            venta.save()
            print "fin venta"
            #detalle_Venta
            for producto in list_products:
                cantidad =  Utilidades().validarIngresoNum(producto.get("cantidad"))
                tipo_precio = producto.get("tipo_precio")
                precio  =  producto.get("precio_unitario").replace(",",".")
                importe = producto.get("importe").replace(",",".")
                producto_id = producto.get("producto_id")
                descripcion = producto.get("descripcion")
                #Saber que  el Producto Existe :[Porsiaca]
                detalle_sucursal_producto = DetalleSucursalAlmacen.objects.get(producto_id = producto_id , sucursal_id = trabajador.sucursal)
                if tipo_precio == "mayor":
                    precio_real = detalle_sucursal_producto.producto_id.precio_x_mayor
                if  tipo_precio == "menor":
                    precio_real = detalle_sucursal_producto.producto_id.precio_x_menor

                if detalle_sucursal_producto.stock  >= cantidad:
                    detalle_sucursal_producto.stock-= cantidad
                    detalle_venta = DetalleVenta(venta_id = venta,detalle_Sucursal_almacen_id = detalle_sucursal_producto , cantidad = cantidad , tipo_precio  =  tipo_precio , precio =precio , importe = importe, descripcion = descripcion , precio_real = precio_real)
                    detalle_venta.save()
                    detalle_sucursal_producto.save()
                    if estado == "NUE":
                        mensaje = "Venta Realiza con Exito"
                    else :
                        mensaje  = "Venta modificada con Exito"
                else:
                    mensaje = "La Cantidad Solicitada del Productos: %s  es Mayor a la del Stock Actual" %(str(detalle_sucursal_producto.producto_id.codigo))
                    raise IntegrityError
                print "fin for"
    except :
        #mensaje = "No se Pudo Agregar la venta , intentelo nuevamente"
        flag = False
        transaction.rollback()
    else:
        transaction.commit()

    finally:
        id_venta  = venta.id
        print">>id_venta"
        print id_venta
        return (id_venta,mensaje,flag)
        #return mensaje


@login_required(login_url='/login/')
def modificar_venta(request):

    if request.method == "GET":
        datos = request.session["datos"]
        if  datos.get("cargo") == "empl":

            try:
                trabajador = SucursalTrabajador.objects.get(trabajador = request.user.id)
            except Exception,e :
                print e

            trabajador_sucursal  = trabajador.sucursal
            try:
                ventas = Venta.objects.filter(sucursal = trabajador_sucursal , estado  = True).order_by('-fecha_emision')
            except Exception,e:
                print e
            template = "homeModificarVentas.html"
            return render_to_response( template , {"ventas":ventas , "trabajador" :trabajador , "datos":datos}, context_instance = RequestContext(request))
        else :
            if datos.get("cargo") == "admi" :
                print "admi"
                return HttpResponseRedirect("/admin/")


@login_required(login_url='/login/')
def cargar_productos(request):
    """
    Por los cambios de la logica en Modificar una  Venta, esta funcion hara la parte previa para preparar los datos a modificar,
    Dichos datos seran enviados por una sesion  a la funcion de "addVenta".
    """

    if request.method == "POST":
        # Obtener el Trabajador para sacarla sucursal
        #trabajador = SucursalTrabajador.objects.get(trabajador = request.user.id)
        dict_products = json.loads(request.POST.get("json_detalle_venta"))
        venta_id = request.POST.get("venta_id")
        request.session["venta_id_to_modificar"] = venta_id
        request.session["detalle_venta_dict_producto"] = dict_products

        # venta = Venta.objects.get(id = venta_id)
        # venta.sucursal
        # venta.estado = False
        # venta.save()

    #     if dict_products:
    #         for producto in dict_products:
    #             cantidad =  Utilidades().validarIngresoNum(producto.get("cantidad"))
    #             producto_id = producto.get("producto_id")
    #             try:
    #                 det_sucu_alm_prod_to_add = DetalleSucursalAlmacen.objects.get(producto_id = producto_id , sucursal_id = venta.sucursal)
    #             except Exception,e:
    #                 print e
    #             det_sucu_alm_prod_to_add.stock += cantidad
    #             det_sucu_alm_prod_to_add.save()
        return HttpResponse("1")
    #     else :
    #         return HttpResponse("0")
    else:
    #     #mensaje = "No se Puede Realizar esta Action"
        return HttpResponse("2")


@login_required(login_url='/login/')
def modificar_detalle_ventas (request,venta_id):

    #FALTA VALIDAR ALGUNOS CAMPOS
    if request.method == "GET":

        try:
            trabajador = SucursalTrabajador.objects.get(trabajador = request.user.id)
        except Exception,e :
            print e
            user = User.objects.get(id =request.user.id)
            if user.is_staff:
                return HttpResponseRedirect("/admin/")
        try:
            venta = Venta.objects.get(id = venta_id , estado = True)
        except Exception ,e :
            print e
            return  HttpResponse("No se puede Acceder a esta Detalle de venta")

        if trabajador.sucursal.id == venta.sucursal.id:

            detalle_venta = DetalleVenta.objects.filter(venta_id = venta_id)
            template = "homeVentas.html"
            modificar = True
            lista_productos = DetalleSucursalAlmacen.objects.filter(sucursal_id = trabajador.sucursal.id)
            datos = request.session["datos"]

            return render_to_response (template , {"trabajador":trabajador,"detalle_venta": detalle_venta , "modificar":modificar,"productos": lista_productos , "ObjVenta" : venta ,"datos":datos} , context_instance = RequestContext(request))
        else :
            return  HttpResponse("ESTE DETALLE PERTENECE A OTRA SUCURSAL")
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------


@login_required(login_url='/login/')
def reporte_asistencia(request):
    if request.method == "GET":
        template = "reporteAsistencia.html"
        try:
            if request.user.is_staff:
                #pero tb redireccionar a la misma plantilla pero con if...si es trabajador o admin
                return HttpResponseRedirect("/admin/")
            elif request.user.is_active:
                asistenciaTodas = AsistenciaTrabajador.objects.all()
                datos = request.session["datos"]

                return render_to_response( template , {"asistencias":asistenciaTodas ,"datos":datos}, context_instance = RequestContext(request))

        except:
            return HttpResponse("")





"""
producto_id
por el momento lo  unico que me interesa  es :

    1.- id producto
    2.- cantidad del  producto
    3.- sucursal
    4.-  ...
"""



# Create your views here.
def iniciarSesion(request):

    template = "signin.html"
    if not request.user.is_authenticated():
        if request.method == "POST":
            iniciar_sesion = FormInciarSesion(request.POST)
            if iniciar_sesion.is_valid():
                user = iniciar_sesion.cleaned_data['username'] #iniciar_sesion.cleaned_data['iniciar_input_email']
                clave = iniciar_sesion.cleaned_data['password']#iniciar_sesion.cleaned_data['iniciar_input_password']
                acceso = authenticate(username=user,password=clave)
                #return redirect("/admin/")
                if acceso is not None:
                    if acceso.is_active:
                        login(request,acceso)

                        session = sessionData(request)

                        if session.get("cargo") == "admi":
                            return HttpResponseRedirect('/admin/')
                        else:
                            if session.get("cargo") == "empl":
                                return HttpResponseRedirect('/ventas/')

                        # try:
                        #     trabajador = SucursalTrabajador.objects.get(trabajador = request.user)
                        #     print trabajador.cargo
                        #     if trabajador.cargo.lower() == "empl":

                        #         request.session["datos"] = {"empresa": trabajador.sucursal.nombre,"nombre":trabajador.trabajador.get_full_name()}

                        #         return HttpResponseRedirect('/ventas/')


                        #     else :
                        #         if trabajador.cargo.lower() == "admi":
                        #             request.session["datos"] = {"empresa": trabajador.sucursal.id_almacen.nombre_empresa,"nombre":trabajador.trabajador.get_full_name()}
                        #             print request.session.datos
                        #             return HttpResponseRedirect('/admin/')

                        # except Exception ,e :
                        #     print e
                        #     print "fail"
                        #     if acceso.is_staff:
                        #         request.session['datos'] = {"empresa": "Administrador","nombre":request.user.get_full_name()}
                        #         return HttpResponseRedirect('/admin/')
                        #     else :
                        #         return render_to_response(template,{'form_iniciar_sesion':iniciar_sesion,'error':'Su cuenta ha sido desactivada,por violar los derechos de uso'},context_instance = RequestContext(request))
                    else:
                        iniciar_sesion = FormInciarSesion(request.POST)
                        return render_to_response(template,{'form_iniciar_sesion':iniciar_sesion,'error':'Su cuenta ha sido desactivada,por violar los derechos de uso'},context_instance = RequestContext(request))
                else:

                    iniciar_sesion = FormInciarSesion(request.POST)
                    return render_to_response(template,{'form_iniciar_sesion':iniciar_sesion,'error':'Por favor Ingrese Correctamente su usuario o password'},context_instance=RequestContext(request))
            else:
                iniciar_sesion = FormInciarSesion(request.POST)
                return render_to_response(template,{'form_iniciar_sesion':iniciar_sesion},context_instance=RequestContext(request))
        else:
            iniciar_sesion = FormInciarSesion(request.POST)
            return render_to_response(template,{'form_iniciar_sesion':iniciar_sesion},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/ventas')



@login_required(login_url='/login/')
def cerrarSesion(request):
    logout(request)
    try:
        del request.session['datos']
    except:
        pass
    return  HttpResponseRedirect('/')


def asistencia(request):
    fecha = datetime.datetime.now()
    if request.method == 'POST':
        try:
            traba = SucursalTrabajador.objects.get(trabajador=request.user)
            tipo = request.POST.get('tipo',"")
            print "post"
            #Asistencia Manana
            if tipo.strip().lower() == "on":
                asistir = AsistenciaTrabajador.objects.filter(Q(hora_ingreso__year=fecha.year) , Q(hora_ingreso__month=fecha.month), Q(hora_ingreso__day=fecha.day) )
                if len(asistir)==1:
                    #actualizar = asistir.get()
                    actualizar = 'Ya se marco hora de ingreso'
                elif len(asistir) == 0:
                    AsistenciaTrabajador.objects.create(trabajador = traba,hora_ingreso=fecha)
                    actualizar = 'Hora de Ingreso registrado'
                else:
                    print "Ha ocurrido un error, duplicidad de data"
                    actualizar = "Ha Ocurrido un error"
            elif tipo.strip().lower() == "off":
                #Asumimos que este es off-Asistencia Salida
                asistir = AsistenciaTrabajador.objects.filter(Q(hora_ingreso__year=fecha.year) , Q(hora_ingreso__month=fecha.month), Q(hora_ingreso__day=fecha.day) )
                if len(asistir) == 1:
                    #code para registrar salida
                    salida = AsistenciaTrabajador.objects.filter(Q(hora_salida__year=fecha.year) , Q(hora_salida__month=fecha.month), Q(hora_salida__day=fecha.day) )
                    if len(salida) == 1:
                        actualizar = 'Ya se marco hora de salida'
                    elif len(salida) == 0:
                        asistir = asistir.get()
                        asistir.hora_salida = fecha
                        asistir.save()
                        actualizar = 'Hora de Salida registrado'
                    else:
                        print "Ha ocurrido un error, duplicidad de data"
                        actualizar = "Ha Ocurrido un error"
                elif len(asistir) == 0:
                    actualizar = "Primero debe de registrar,su Ingreso"
                else:
                    print "Ha ocurrido un error, duplicidad de data"
                    actualizar = "Ha Ocurrido un error"
        except Exception, e:
            print "fallo"
            print e
            actualizar = "Ha ocurrido un error"
        return HttpResponse(actualizar)
    else:
        template = "asistencia.html"
        datos = request.session["datos"]

        return render_to_response(template,{"datos": datos},context_instance=RequestContext(request))


@login_required(login_url='/login/')
def home_empleado_menu_reporte(request):
    if request.method == "GET":
        if request.user.is_staff:
            return HttpResponseRedirect("/admin/")

        elif  request.user.is_active:
            try:
                trabajador =  SucursalTrabajador.objects.get(trabajador = request.user.id)
            except Exception, e:
                print e

            template = "homeEmpleadoReporte.html"
            datos = request.session["datos"]

            return render_to_response(template , {"trabajador":trabajador , "datos":datos} , context_instance=RequestContext(request) )
        else :
            return HttpResponse("ERROR ")
    else :
        return HttpResponse("Error")


@login_required(login_url='/login/')
def reporte_venta (request):
    if request.method == "GET":
        if request.user.is_staff:
            return HttpResponseRedirect("/admin/")

        elif  request.user.is_active:
            try:
                trabajador =  SucursalTrabajador.objects.get(trabajador = request.user.id)
            except Exception, e:
                print e
                return HttpResponse("error")

            template = "homeEmpleadoReporteVentas.html"
            ventas = Venta.objects.filter(sucursal = trabajador.sucursal.id , estado  = True).order_by('-fecha_emision')
            datos = request.session["datos"]

            return render_to_response(template , {"trabajador":trabajador , "ventas":ventas , "datos":datos} , context_instance=RequestContext(request) )
        else :
            return HttpResponse("ERROR ")
    else :
        return HttpResponse("Error")



def detalle_venta(request):
    if request.method  == "GET":
        if request.user.is_staff:
            return HttpResponseRedirect("/admin/")
        elif  request.user.is_active:
            try:
                trabajador =  SucursalTrabajador.objects.get(trabajador = request.user.id)
            except Exception, e:
                print e
                return HttpResponse("error")
            codido =Utilidades().validarIngresoNum(request.GET.get("codigo"))
            try:
                venta = Venta.objects.get(id = codido)
            except Exception, e:
                print e
                HttpResponse("Error")

            if trabajador.sucursal.id == venta.sucursal.id:
                det = DetalleVenta.objects.filter(venta_id = venta.id)
                if det:

                    data = [Utilidades().detalle_venta_to_json(detalle) for detalle in det]
                else :

                    data = []

                return HttpResponse( json.dumps(data) , content_type='application/json')

def sessionData(request):
    print "datos"
    print "datos" in request.session
    #print request.session['datos']

    if "datos" in request.session:
        return request.session['datos']
    else:
        try:
            trabajador = SucursalTrabajador.objects.get(trabajador = request.user)

            name_to_show = trabajador.trabajador.get_full_name()
            if name_to_show == '':
                name_to_show = trabajador.trabajador.username


            if trabajador.cargo.lower() == "empl":
                request.session["datos"] = {"empresa": trabajador.sucursal.nombre,"nombre":name_to_show, "cargo" : trabajador.cargo}
            else :
                if trabajador.cargo.lower() == "admi":
                    request.session["datos"] = {"empresa": trabajador.sucursal.id_almacen.nombre_empresa,"nombre":name_to_show,"cargo" : trabajador.cargo}
        except Exception ,e :

            try:
                if not request.user.is_anonymous() :
                    if request.user.is_staff:
                        name_to_show = request.user.get_full_name()
                        print "name to show " , name_to_show
                        if name_to_show == '':

                            name_to_show=request.user.username
                        request.session['datos'] = {"empresa": "Administrador","nombre":name_to_show,"cargo":"admi"}

                else :
                    return HttpResponseRedirect("/login")

            except Exception ,e   :
                print e

        return request.session['datos']



@login_required(login_url='/login/')
def imprimirVenta(request,venta_id):
    

    if request.method == "GET":
        
        print "GET"

        venta = None
        #id_venta  = request.GET.get("venta_id",0)
        trabajador = None
        try:
            trabajador =  SucursalTrabajador.objects.get(trabajador = request.user.id)
        except Exception, e:
            user = User.objects.get(id =request.user.id)
            if user.is_staff:
                return HttpResponseRedirect("/admin/")
        

        try:
            venta = Venta.objects.get(id= venta_id)
            print "venta",venta
        except Exception, e:
            print e


        if trabajador.sucursal.id == venta.sucursal.id:
            try:
                detalle_venta = DetalleVenta.objects.filter(venta_id=venta)
                print "detalle_venta" ,detalle_venta
            except Exception, e:
                print e

            datos = request.session['datos']
            template = 'imprimir.html'
            return render_to_response(template,{'venta':venta,'detalle_venta':detalle_venta,'datos':datos},context_instance=RequestContext(request))


    





















