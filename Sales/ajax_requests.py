from django.db.models import Avg, Max, Min, Sum
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import path
from Sales.models import Terceros, InfoProductos, Productos, Compras, Compras_General, Ventas, TicketsPOS

def ajax_infoproductos(request):

    if request.is_ajax():
        if request.method == 'GET':
            producto = request.GET.get('producto')
            obj_producto = InfoProductos.objects.filter(pk=producto)
            obj_producto=serializers.serialize('json',obj_producto)
            data={
                'infoproducto':obj_producto
            }
            return JsonResponse(data)

def ajax_infoticket(request):
    
    if request.is_ajax():
        if request.method == 'GET':
            nroticket = request.GET.get('ticket')
            detalle_ticket = Ventas.objects.filter(docventa=nroticket)
            detalle_ticket = serializers.serialize('json',detalle_ticket)
            obj_ticket=TicketsPOS.objects.filter(pk=nroticket)
            obj_ticket=serializers.serialize('json',obj_ticket)
            data={
                'productos_ticket':detalle_ticket,
                'info_ticket':obj_ticket
            }
            
            return JsonResponse(data)


urls =[
        path('infoproductos',ajax_infoproductos,name='ajax_infoproductos'),
        path('infoticket',ajax_infoticket,name='ajax_infoticket'),
    ]
    