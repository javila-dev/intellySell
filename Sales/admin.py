from django.contrib import admin
from Sales.models import Productos,Terceros,Ventas,TicketsPOS,Compras,Compras_General, Devoluciones,Pagos_Clientes
# Register your models here.

class adminProductos(admin.ModelAdmin):
    list_display=['codigo','nombre','nombrealterno','codigoalterno','ubicacion','precio']
class adminTerceros(admin.ModelAdmin):
    list_display=['identificacion','nombre','direccion','celular']
class adminTicketsPOS(admin.ModelAdmin):
    list_display=['idTicket','fecha','valor','estado','cierre']
    list_filter=['fecha','estado']
class adminDevolucion(admin.ModelAdmin):
    list_display=['pk','fecha','valor','ticket','cierre']
    list_filter=['fecha']
class adminPagos(admin.ModelAdmin):
    list_display=['pk','fecha','documento','valor','usuario']
    list_filter=['fecha']

admin.site.register(Productos,adminProductos)
admin.site.register(Terceros,adminTerceros)
admin.site.register(TicketsPOS,adminTicketsPOS)
admin.site.register(Devoluciones,adminDevolucion)
admin.site.register(Pagos_Clientes,adminPagos)