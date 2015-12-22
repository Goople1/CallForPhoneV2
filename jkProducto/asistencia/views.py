from django.shortcuts import  render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect ,HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import AsistenciaTrabajador
from sucursales.models import SucursalTrabajador
#from sucursales.utilidades import Utilidades
import datetime
# Create your views here.

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

@login_required(login_url='/login/')
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
        print "get"
        template = "asistencia.html"
        datos = request.session["datos"]

        return render_to_response(template,{"datos": datos},context_instance=RequestContext(request))

