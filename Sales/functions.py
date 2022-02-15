from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Max, Min, Sum
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
#Importar modulos adicionales
import datetime
import json
#Importar Modelos
from Sales.models import (Productos, HistoryLine, Compras, AjustesInventario,
                          Terceros, Compras_General
                          )

#Importar Formularios
from Sales.forms import (form_DatosProducto, form_AjustesInv, form_Tercero,
                         form_nuevaCompra
                         )

def NuevoProducto(request,form):
    """
    Esta funcion crea un producto nuevo a partir del request de la vista y el form (form_nuevoProducto) luego de ser validado
    """
    descripcion = form.cleaned_data.get('Descripcion')
    codigo_alterno = form.cleaned_data.get('Codigo_Alterno')
    nombre_alterno = form.cleaned_data.get('Nombre_Alterno')
    precio = form.cleaned_data.get('Precio')
    marca = form.cleaned_data.get('Marca')
    ubicacion = form.cleaned_data.get('Ubicacion')
    
    obj_producto = Productos.objects.create(nombre=descripcion,codigoalterno=codigo_alterno,
                                            nombrealterno=nombre_alterno,precio=precio,marca=marca,ubicacion=ubicacion,
                                            fechacreacion=datetime.date.today(),estado='Activo')
    codigo=Productos.objects.last().pk
    HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                            modulo='Inventario',accion=f'Creó el articulo {descripcion} ({codigo})')
    
    