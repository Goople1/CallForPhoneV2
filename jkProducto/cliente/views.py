from django.shortcuts import render, HttpResponse
import json

from sucursales.utilidades import Utilidades
from .models import Cliente
# Create your views here.


def buscarCliente(request):	
    print "buscarCliente"
    response_data = {}
    if request.method == "POST":
        clienteSearch = {}
        try:
            rucDni = request.POST.get("txtDocumentoAux")  	
            clienteSearch = Cliente.objects.filter(ruc_dni = rucDni)
            if len(clienteSearch) > 0:
                clienteSearch = clienteSearch[0]
                clienteSearch = Utilidades().cliente_to_json(clienteSearch)
                response_data['data'] = clienteSearch
                response_data['result'] = 'correcto'
            else:
                response_data['data'] = {}
                response_data['message'] = 'No se encontro informacion, con el dato proporcionado.'
                response_data['result'] = 'correctoVacio'
                #print json.dumps(clienteSearch)
                #print
                print "todo dick"
                #print json.dumps(response_data)
        except Exception, e:
            print "error"
            print e
            response_data['message'] = 'Error del Servidor'
            response_data['result'] = 'errorServer'
        return HttpResponse( json.dumps(response_data) , content_type='application/json')  	    	    			
    else:
        response_data['result'] = 'errorServer'
        response_data['message'] = 'No acepta peticiones Get'    	    	    	
        return HttpResponse( json.dumps(response_data) , content_type='application/json')