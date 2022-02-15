#Importar modulos Django
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required
from django.db.models import Avg, Max, Min, Sum, Count, Q, F, Subquery, OuterRef
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

#Importar modulos adicionales
import datetime
import json
#Importar Modelos
from Sales.models import (Productos, HistoryLine, Compras, AjustesInventario,
                          Terceros, Compras_General, InfoProductos, Ventas, TicketsPOS,
                          Consecutivos, Pagos_Clientes, SesionPOS, Devoluciones, AjustesCaja
                          )
#Importar Proxys
from Sales.models import (ProxyTickets)
#Importar Formularios
from Sales.forms import (form_DatosProducto, form_AjustesInv, form_Tercero,
                         form_nuevaCompra, form_NuevoProducto
                         )

#Importar Funciones
from Sales.functions import (NuevoProducto)

# Create your views here.
@login_required(login_url='/accounts/login')
def welcome(request):
    
    datos_clientes=TicketsPOS.objects.raw('CALL estados_cuenta("")')
    paginator_deuda = Paginator(datos_clientes,6)
    page_number=request.GET.get('page')
    obj_clientes=paginator_deuda.get_page(page_number)
    
    obj_sesiones = SesionPOS.objects.all()
    ultima_sesion = obj_sesiones.last()
    estado='Sin informacion'
    if ultima_sesion!=None:
        if ultima_sesion.fecha_cierre is not None:
            estado=f'Cerrada el {ultima_sesion.fecha_cierre.date()} a las {ultima_sesion.fecha_cierre.time()} por {ultima_sesion.usuario_cierre}'
        else: estado=f'Abierta el {ultima_sesion.fecha_apertura.date()} a las {ultima_sesion.fecha_apertura.time()} por {ultima_sesion.usuario_apertura}'
    obj_compras=Compras_General.objects.filter(estado='Pendiente').count()
    obj_history=HistoryLine.objects.all().order_by('-pk')[:4]
    
    obj_sinterminar=TicketsPOS.objects.filter(estado='Pendiente').count()
    
    context={
        'clientes':obj_clientes,
        'sesionPOS':estado,
        'compras_sin_aprobar':obj_compras,
        'ultimasAcciones':obj_history,
        'sin_terminar':obj_sinterminar,
    }
    return render(request,'landing_page.html',context)

@login_required(login_url='/accounts/login')
def data_kardex(request,codigo_producto):
    obj_compras = Compras.objects.filter(producto=codigo_producto)
    data_compras = serializers.serialize('json',obj_compras)
    """ data_compras.append({"draw":1,"recordsTotal":len(data_compras),"recordsFiltered":len(data_compras)})
    print(data_compras) """
    return HttpResponse(data_compras, content_type='application/json')

@login_required(login_url='/accounts/login')
def Nuevo_Tercero(request):
    context={
        'form_Terceros':form_Tercero,
    }
    if request.is_ajax():
        if request.method == 'GET':
            identificacion = request.GET.get('identificacion')
            exists=Terceros.objects.filter(identificacion=identificacion).exists()
            data={'exists':exists}
            return JsonResponse(data)
    if request.method == 'POST':
        form=form_Tercero(request.POST)
        if form.is_valid():
            identificacion=form.cleaned_data.get('Identificacion')
            nombre=form.cleaned_data.get('Nombre')
            tipo=form.cleaned_data.get('Tipo')
            direccion=form.cleaned_data.get('Direccion')
            telefono1=form.cleaned_data.get('Telefono_1')
            telefono2=form.cleaned_data.get('Telefono_2')
            
            Terceros.objects.create(nombre=nombre,estado='Activo',identificacion=identificacion,
                                    direccion=direccion,telefono=telefono2,celular=telefono1,tipo=tipo)
            
            accion=f'Creó el {tipo} {nombre} ({identificacion})'
            HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Terceros',accion=accion)
            context['alerta']=True
            context['msj']='Se creo el tercero con exito'
    return render(request,'terceros.html',context)

@permission_required('Sales.add_compras', raise_exception=True)
def Nueva_Compra(request):
    obj_productos = InfoProductos.objects.all()
    obj_terceros = Terceros.objects.filter(estado='Activo')
    context={
        'form':form_nuevaCompra,
        'form_NuevoProducto':form_NuevoProducto,
        'productos':obj_productos,
        'terceros':obj_terceros,
    }
    if request.is_ajax():
        if request.method == 'GET':
            codigo = request.GET.get('producto')
            obj_producto = Productos.objects.filter(codigo=codigo)
            obj_producto = serializers.serialize('json',obj_producto)
            obj_costo = Compras.objects.filter(producto=codigo)
            if obj_costo.exists():
                obj_costo = obj_costo.last().valor
            else: obj_costo=0
            data={
                'info_producto':obj_producto,
                'info_costo':obj_costo,
            }
            return JsonResponse(data)
        if request.method == 'POST':
            form=form_NuevoProducto(request.POST)
            if form.is_valid():
                NuevoProducto(request,form)
                codigo=Productos.objects.last().pk
                descripcion = form.cleaned_data.get('Descripcion')
                precio = form.cleaned_data.get('Precio')
                passed=True
                data={
                    'passed':passed,
                    'codigo':codigo,
                    'descripcion':descripcion,
                    'precio':precio,
                }
                return JsonResponse(data)
    if request.method == 'POST':
        proveedor = request.POST.get('proveedorId')
        nombreProveedor = request.POST.get('nombreProveedor')
        nroFactura = request.POST.get('nroFactura')
        fechaFactura = request.POST.get('Fecha_Factura')
        codigos = request.POST.getlist('codigoDetalle')
        cantidad = request.POST.getlist('cantidadDetalle')
        costo = request.POST.getlist('costoDetalle')
        totales = request.POST.getlist('totalDetalle')
        nuevoPVP = request.POST.getlist('nuevoPVPDetalle')
        
        TotalCompra=0
        for i in totales:
            TotalCompra += int(i)
        
        Compras_General.objects.create(fecha=fechaFactura,valor=TotalCompra,usuario=request.user,
                                        nroFactura=nroFactura,proveedor=Terceros.objects.get(identificacion=proveedor),estado='Pendiente')
        doc_compra=Compras_General.objects.get(nroFactura=nroFactura,proveedor=proveedor)
        for i in range(0,len(codigos)):
            Compras.objects.create(producto=Productos.objects.get(codigo=codigos[i]),fecha=fechaFactura,cantidad=int(cantidad[i]),
                                    valor=int(costo[i]),doccompra=Compras_General.objects.get(pk=doc_compra.pk))
            producto = Productos.objects.get(pk=codigos[i])
            try:
                if producto.precio!=int(nuevoPVP[i]): 
                    accion=f'Cambió el precio del producto {producto.nombre} ({codigos[i]}) en la compra con numero de factura {nroFactura}'
                    HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                                modulo='Compras',accion=accion)
                    producto.precio=int(nuevoPVP[i])
                    producto.save()
            except: pass
            
        accion=f'Registró una compra de {nombreProveedor} ({proveedor}) por ${TotalCompra} numero de factura {nroFactura}'
        HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='Compras',accion=accion)
        mensaje_alerta='La compra fue registrada con exito, recuerda solicitar su aprobacion para envio a cuentas por pagar'
        context['alerta']=True
        context['tipo_alerta']='success'
        context['mensaje_alerta']=mensaje_alerta
        
    return render(request,'nueva_compra.html',context)

@permission_required('Sales.change_compras', raise_exception=True)
def Modificar_Compra(request,proveedor,factura):
    
    obj_productos = InfoProductos.objects.filter(estado='Activo')
    obj_terceros = Terceros.objects.filter(estado='Activo')
    obj_compra = Compras_General.objects.get(proveedor=proveedor,nroFactura=factura)
    obj_proveedor = Terceros.objects.get(identificacion=proveedor)
    compras = Compras.objects.filter(doccompra=obj_compra.pk)
    data_compra = {}
    i=0
    for compra in compras:
        data_compra[i]= {
            'producto' : compra.producto.pk,
            'descripcion' : compra.producto.nombre,
            'cantidad' : compra.cantidad,
            'costo' : compra.valor,
            'total' : compra.cantidad*compra.valor,
            'precio' : compra.producto.precio,
        }
        i+=1
    data_compra['len']=len(compras)
    detalle_compra = json.dumps(data_compra )
    context={
        'form':form_nuevaCompra,
        'form_NuevoProducto':form_NuevoProducto,
        'productos':obj_productos,
        'terceros':obj_terceros,
        'datos_compra':obj_compra,
        'detalle_compra':detalle_compra,
        'proveedor':obj_proveedor,
        'factura':factura,
        'modificar':True,
    }

    if request.method == 'POST':
        proveedor = request.POST.get('proveedorId')
        nombreProveedor = request.POST.get('nombreProveedor')
        nroFactura = request.POST.get('nroFactura')
        fechaFactura = request.POST.get('Fecha_Factura')
        codigos = request.POST.getlist('codigoDetalle')
        cantidad = request.POST.getlist('cantidadDetalle')
        costo = request.POST.getlist('costoDetalle')
        totales = request.POST.getlist('totalDetalle')
        nuevoPVP = request.POST.getlist('nuevoPVPDetalle')

        TotalCompra=0
        for i in totales:
            TotalCompra += int(i)
        compra_general = Compras_General.objects.get(proveedor=proveedor,nroFactura=nroFactura)
        compra_general.valor=TotalCompra
        compra_general.proveedor=Terceros.objects.get(identificacion=proveedor)
        compra_general.fecha=fechaFactura
        compra_general.save()
        obj_compra = Compras.objects.filter(doccompra=compra_general.pk)
        for compra in obj_compra:
            compra.delete()
        for i in range(0,len(codigos)):
            Compras.objects.create(producto=Productos.objects.get(codigo=codigos[i]),fecha=fechaFactura,cantidad=int(cantidad[i]),
                                    valor=int(costo[i]),doccompra=Compras_General.objects.get(pk=compra_general.pk))
        
        accion=f'Modificó la compra de {nombreProveedor} ({proveedor}) por ${TotalCompra} numero de factura {nroFactura}'
        HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='Compras',accion=accion)
        
        return HttpResponseRedirect("/compras/todas/Pendiente")


    return render(request,'nueva_compra.html',context)

@login_required(login_url='/accounts/login')
def transito_compras(request):
    obj_productos = Compras.objects.filter(doccompra__estado="Pendiente")
    context={
        'productos':obj_productos,
    }

    return render(request,'transito_compras.html',context)

@login_required(login_url='/accounts/login')
def lista_compras(request,estado):
    obj_compras=Compras_General.objects.filter(estado=estado).select_related('proveedor')
    context={
        'compras':obj_compras,
        'estado':estado,
    }
    if request.method == 'POST':
        nit=request.POST.get('proveedor')
        fact=request.POST.get('factura')
        obj_compra=Compras_General.objects.get(proveedor=nit,nroFactura=fact)
        obj_compra.estado='Aprobado'
        obj_compra.save()

        mensaje_alerta=f'La factura {fact} fué aprobada y ya se encuentra en el modulo de pagos'
        context['alerta']=True
        context['tipo_alerta']='success'
        context['mensaje_alerta']=mensaje_alerta


    return render(request,'lista_compras.html',context)

@login_required(login_url='/accounts/login')
def lista_terceros(request):
    obj_terceros=Terceros.objects.filter(estado='Activo')
    context = {
        'terceros':obj_terceros,
        'form_Terceros':form_Tercero
    }
    if request.method == 'POST':
        form=form_Tercero(request.POST)
        if form.is_valid():
            identificacion=form.cleaned_data.get('Identificacion')
            nombre=form.cleaned_data.get('Nombre')
            tipo=form.cleaned_data.get('Tipo')
            direccion=form.cleaned_data.get('Direccion')
            telefono1=form.cleaned_data.get('Telefono_1')
            telefono2=form.cleaned_data.get('Telefono_2')

            obj_tercero=Terceros.objects.get(identificacion=identificacion)
            obj_tercero.nombre=nombre
            obj_tercero.direccion=direccion
            obj_tercero.telefono2=telefono2
            obj_tercero.telefono1=telefono1
            obj_tercero.tipo=tipo
            obj_tercero.save()
            
            accion=f'Modificó el {tipo} {nombre} ({identificacion})'
            HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Terceros',accion=accion)
            mensaje_alerta=f'¡El tercero {nombre} ({identificacion}) fué modificado con exito!'
            context['alerta']=True
            context['tipo_alerta']='success'
            context['mensaje_alerta']=mensaje_alerta
    
    obj_terceros=Terceros.objects.filter(estado='Activo')
    context['terceros']=obj_terceros

    return render(request,'lista_terceros.html',context)

@login_required(login_url='/accounts/login')
def lista_productos(request,estado):
    obj_historyline = HistoryLine.objects
    obj_productos = InfoProductos.objects.filter(estado=estado)
    #obj_productos = Productos.objects.raw('CALL vista_productos()')
    #obj_productos = Productos.objects.filter(estado='Activo')
    context={
        'form_DatosProducto':form_DatosProducto,
        'form_NuevoProducto':form_NuevoProducto,
        'form_AjustesInv':form_AjustesInv,
        'productos':obj_productos,
        'estado':estado,
    }
    if request.is_ajax():
        if request.method == 'GET':
            call=request.GET.get('call')
            if call == 'data_productos':
                codigo = request.GET.get('codigo')
                obj_producto = Productos.objects.filter(codigo=codigo)
                obj_kardex = Compras.objects.raw(f'CALL kardex("{codigo}")')
                kardex=[]
                for obj in obj_kardex:
                    kardex.append({
                        "pk":obj.pk,
                        "producto":obj.Producto,
                        "fecha":obj.Fecha,
                        "descripcion":obj.Descripcion,
                        "usuario":obj.usuario,
                        "debitos":obj.Debitos,
                        "creditos":obj.Creditos
                    })
                data = serializers.serialize('json',obj_producto)
                return JsonResponse({'data':data,'kardex':kardex})
            elif call == 'costo_producto':
                codigo = request.GET.get('codigo')
                tipo = request.GET.get('tipo').capitalize()
                if Compras.objects.filter(producto=codigo).exists():
                    if tipo == 'Ultimo':
                        obj_costo = Compras.objects.filter(producto=codigo).last()
                        costo = obj_costo.valor
                    elif tipo == 'Promedio':
                        obj_costo = Compras.objects.filter(producto=codigo).aggregate(Avg('valor'))
                        costo = obj_costo['valor__avg']
                    elif tipo == 'Maximo':
                        obj_costo = Compras.objects.filter(producto=codigo).aggregate(Max('valor'))
                        costo = obj_costo['valor__max']
                    data={
                        'costo':costo
                    }
                    return JsonResponse(data)
    if request.method == 'POST':
        if request.POST.get('btnguardarDatos'):
            form=form_DatosProducto(request.POST)
            if form.is_valid():
                codigo = form.cleaned_data.get('Codigo')
                descripcion = form.cleaned_data.get('Descripcion')
                codigo_alterno = form.cleaned_data.get('Codigo_Alterno')
                nombre_alterno = form.cleaned_data.get('Nombre_Alterno')
                precio = form.cleaned_data.get('Precio')
                marca = form.cleaned_data.get('Marca')
                ubicacion = form.cleaned_data.get('Ubicacion')
                
                obj_producto = Productos.objects.get(codigo=codigo)
                obj_producto.nombre = descripcion
                obj_producto.codigoalterno = codigo_alterno
                obj_producto.nombrealterno = nombre_alterno
                obj_producto.precio = precio
                obj_producto.marca = marca
                obj_producto.ubicacion = ubicacion
                obj_producto.save()
                
                obj_historyline.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Inventario',accion=f'Modificó el articulo {descripcion}')
        if request.POST.get('btnAjustar'):
            check_perms(request,('Sales.change_ventas',))
            form=form_AjustesInv(request.POST)
            if form.is_valid():
                codigo=form.cleaned_data.get('Codigo_ajuste')
                tipo_ajuste=form.cleaned_data.get('Tipo_ajuste')
                cantidad=form.cleaned_data.get('Cantidad')
                if tipo_ajuste=='Credito': cantidad*=-1
                descripcion=form.cleaned_data.get('descripAjuste')
                object_producto = Productos.objects.get(pk=codigo)
                obj_ajustes=AjustesInventario.objects.create(prod_ajuste=object_producto,fecha=datetime.date.today(),
                                                             usuario=request.user,concepto=descripcion,
                                                             cantidad=cantidad)
                accion=f'Realizó un ajuste de inventario al articulo {descripcion} ({codigo}) de {cantidad} unidades'
                obj_historyline.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Inventario',accion=accion)
        if request.POST.get('btnInactivar'):
            form=form_DatosProducto(request.POST)
            if form.is_valid():
                codigo = form.cleaned_data.get('Codigo')
                descripcion = form.cleaned_data.get('Descripcion')
                stock = form.cleaned_data.get('Stock')
                if int(stock)<=0:
                    obj_producto = Productos.objects.get(codigo=codigo)
                    obj_producto.estado = 'Inactivo'
                    obj_producto.save()
                    
                    accion=f'Inactivo el producto {descripcion} ({codigo})'
                    obj_historyline.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Inventario',accion=accion)
                else:
                    mensaje_alerta = 'Para inactivar un producto este no debe tener stock'
                    context['alerta']=True
                    context['tipo_alerta']='warning'
                    context['mensaje_alerta']=mensaje_alerta
        if request.POST.get('btnActivar'):
            form=form_DatosProducto(request.POST)
            if form.is_valid():
                codigo = form.cleaned_data.get('Codigo')
                descripcion = form.cleaned_data.get('Descripcion')
                obj_producto = Productos.objects.get(codigo=codigo)
                obj_producto.estado = 'Activo'
                obj_producto.save()
                
                accion=f'Reactivo el producto {descripcion} ({codigo})'
                obj_historyline.create(fecha=datetime.date.today(),usuario=request.user,
                                       modulo='Inventario',accion=accion)
        if request.POST.get('btnNuevoProducto'):
            form=form_NuevoProducto(request.POST)
            if form.is_valid():
                NuevoProducto(request,form)
                mensaje_alerta=f'¡El producto {request.POST.get("Descripcion")} fué creado con exito!'
                context['alerta']=True
                context['tipo_alerta']='success'
                context['mensaje_alerta']=mensaje_alerta
    
    return render(request,'lista_productos.html',context)

@login_required(login_url='/accounts/login')
def pos(request):
    
    obj_sesiones = SesionPOS.objects.all()
    ultima_sesion = obj_sesiones.last()
    ultima_sesion.usuario_apertura
    if ultima_sesion!=None:
        if ultima_sesion.fecha_cierre is not None:
            mensaje=f'No se puede crear un ticket sin abrir una sesion POS primero'
            return alertas(request,'error',mensaje)
    
    obj_terceros = Terceros.objects.filter(estado='Activo')
    context={
        'terceros':obj_terceros,
        'nroticket':"0000000",
    }
    
    if request.method == 'POST':
        if request.POST.get('btnCobrarTicket'):
            nro_ticket = request.POST.get('nroTicket')
            cliente=request.POST.get('idCliente')
            obj_cliente=Terceros.objects.get(pk=cliente)
            total_ticket=request.POST.get('totalCobro')
            if nro_ticket != "0000000":
                obj_ticket=TicketsPOS.objects.get(pk=nro_ticket)
                obj_ticket.estado='Terminado'
                obj_ticket.usuario=str(request.user)
                obj_ticket.valor=total_ticket
                obj_ticket.cliente=obj_cliente
                obj_ticket.save()
                ticket=obj_ticket
            else:
                TicketsPOS.objects.create(estado='Terminado',fecha=datetime.date.today(),cliente=obj_cliente,
                                            usuario=request.user,valor=total_ticket)
                ticket=TicketsPOS.objects.last()            
            Pagos_Clientes.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                          valor=total_ticket,documento=ticket)
            productos = request.POST.getlist('codigoDetalle')
            cantidades = request.POST.getlist('cantidadDetalle')
            valores = request.POST.getlist('precioDetalle')
            if nro_ticket != "0000000":
                obj_detalleproductos=Ventas.objects.filter(docventa=nro_ticket)
                for producto in obj_detalleproductos:
                    producto.delete()
            for i in range(0,len(productos)):
                producto=Productos.objects.get(pk=productos[i])
                Ventas.objects.create(fecha=datetime.date.today(),
                                      producto=producto,
                                      valor=valores[i],
                                      cantidad=cantidades[i],
                                      docventa=ticket)
            
            mensaje_alerta=f'Se creó el ticket de venta Nº{ticket.pk}'
            context['alerta']=True
            context['tipo_alerta']='success'
            context['mensaje_alerta']=mensaje_alerta
        if request.POST.get('btnDejarPendiente'):
            nro_ticket = request.POST.get('nroTicket')
            cliente=request.POST.get('idCliente')
            obj_cliente=Terceros.objects.get(pk=cliente)
            total_ticket=request.POST.get('totalCobro')
            productos = request.POST.getlist('codigoDetalle')
            cantidades = request.POST.getlist('cantidadDetalle')
            valores = request.POST.getlist('precioDetalle')
            if nro_ticket != "0000000":
                obj_ticket=TicketsPOS.objects.get(pk=nro_ticket)
                obj_ticket.estado='Pendiente'
                obj_ticket.usuario=request.user
                obj_ticket.valor=total_ticket
                obj_ticket.cliente=obj_cliente
                obj_ticket.save()
                ticket=obj_ticket
            else:
                TicketsPOS.objects.create(estado='Pendiente',fecha=datetime.date.today(),cliente=obj_cliente,
                                            usuario=request.user,valor=total_ticket)
                ticket=TicketsPOS.objects.last()
            if nro_ticket != "0000000":
                obj_detalleproductos=Ventas.objects.filter(docventa=nro_ticket)
                for producto in obj_detalleproductos:
                    producto.delete()
            for i in range(0,len(productos)):
                producto=Productos.objects.get(pk=productos[i])
                Ventas.objects.create(fecha=datetime.date.today(),
                                      producto=producto,
                                      valor=valores[i],
                                      cantidad=cantidades[i],
                                      docventa=ticket)
            accion=f'Dejó pendiente el ticket de venta Nº{ticket} del tercero {cliente}'
            HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='POS',accion=accion)
            mensaje_alerta=f'se dejó pendiente el ticket de venta Nº{ticket.pk}'
            context['alerta']=True
            context['tipo_alerta']='success'
            context['mensaje_alerta']=mensaje_alerta
        if request.POST.get('btnEnviarCta'):
            nro_ticket = request.POST.get('nroTicket')
            cliente=request.POST.get('idCliente')
            obj_cliente=Terceros.objects.get(pk=cliente)
            total_ticket=request.POST.get('totalCobro')
            if nro_ticket != "0000000":
                obj_ticket=TicketsPOS.objects.get(pk=nro_ticket)
                obj_ticket.estado='Terminado'
                obj_ticket.usuario=request.user
                obj_ticket.valor=total_ticket
                obj_ticket.cliente=obj_cliente
                obj_ticket.save()
                ticket=obj_ticket
            else:
                TicketsPOS.objects.create(estado='Terminado',fecha=datetime.date.today(),cliente=obj_cliente,
                                            usuario=request.user,valor=total_ticket)
                ticket=TicketsPOS.objects.last()
            abonado = request.POST.get('dineroAbonado')
            if int(abonado) > 0:
                Pagos_Clientes.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                            valor=abonado,documento=ticket)
            productos = request.POST.getlist('codigoDetalle')
            cantidades = request.POST.getlist('cantidadDetalle')
            valores = request.POST.getlist('precioDetalle')
            if nro_ticket != "0000000":
                obj_detalleproductos=Ventas.objects.filter(docventa=nro_ticket)
                for producto in obj_detalleproductos:
                    producto.delete()
            for i in range(0,len(productos)):
                producto=Productos.objects.get(pk=productos[i])
                Ventas.objects.create(fecha=datetime.date.today(),
                                      producto=producto,
                                      valor=valores[i],
                                      cantidad=cantidades[i],
                                      docventa=ticket)
            accion=f'Envió el ticket de venta Nº{ticket} del tercero {cliente} a cuenta'
            HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='POS',accion=accion)
            mensaje_alerta=f'Se envió a cuenta el ticket de venta Nº{ticket.pk}'
            context['alerta']=True
            context['tipo_alerta']='success'
            context['mensaje_alerta']=mensaje_alerta
        if request.POST.get('btnAnular'):
            nro_ticket = request.POST.get('nroTicket')   
            obj_ticket=TicketsPOS.objects.get(pk=nro_ticket)
            obj_productos = Ventas.objects.filter(docventa=nro_ticket)
            for producto in obj_productos:
                producto.delete()
            obj_ticket.estado='Anulado'
            obj_ticket.valor=0
            obj_ticket.save()
            mensaje_alerta=f'El ticket Nº{nro_ticket} fue anulado'
            context['alerta']=True
            context['tipo_alerta']='success'
            context['mensaje_alerta']=mensaje_alerta
    obj_productos = Productos.objects.filter(estado='Activo').annotate(
        stock = Sum('compras__cantidad')-Sum('ventas__cantidad')+Sum('ajustesinventario__cantidad'),
        costo_promedio = F('compras__cantidad')*F('compras__valor')/Sum(F('compras__cantidad')),
        costo_maximo = Max('compras__valor'),
        costo_minimo = Min('compras__valor'),
        compras_cantidad = Sum('compras__cantidad'),
        ventas_cantidad = Sum('ventas__cantidad'),
        ajustes_cantidad = Sum('ajustesinventario__cantidad')
    )
    context['productos']=obj_productos
    obj_ticketsPdtes = TicketsPOS.objects.filter(estado='Pendiente')
    context['ticketsPdtes']=obj_ticketsPdtes

    return render(request,'pos.html',context)

@login_required(login_url='/accounts/login')
def abrir_sesion_pos(request):
    
    obj_sesiones = SesionPOS.objects.all()
    ultima_sesion = obj_sesiones.last()
    if ultima_sesion!=None:
        if ultima_sesion.fecha_cierre is None:
            mensaje=f'No se puede crear una nueva sesion si no se ha cerrado la anterior, la sesion {ultima_sesion.pk} abierta por {ultima_sesion.usuario_apertura} aun esta abierta.'
            return alertas(request,'error',mensaje)
    
    
    context={
        
    }
    
    if request.method == 'POST':
        base=request.POST.get('base')
        apertura=datetime.datetime.now()
        SesionPOS.objects.create(fecha_apertura=apertura,usuario_apertura=request.user,
                                 base=base)
        return HttpResponseRedirect('/ventas/pos/nuevo')
        
    return render(request,'modal_abrirPOS.html',context)

@login_required(login_url='/accounts/login')
def ver_ticket(request,ticket):
    
    obj_ticket=TicketsPOS.objects.get(pk=ticket)
    detalle_productos=Ventas.objects.select_related('producto').filter(docventa=ticket)
    detalle_productos=serializers.serialize('json',detalle_productos)
    
    context={
        'ticket':ticket,
        'obj_ticket':obj_ticket,
        'productos':detalle_productos,
    }
    
    return render(request,'ver_ticket.html',context)

@login_required(login_url='/accounts/login')
def lista_tickets(request):
    
    obj_tickets=ProxyTickets.objects.all().order_by('-pk')
    context={
        'tickets':obj_tickets
    }
    
    return render(request,'lista_tickets.html',context)

@login_required(login_url='/accounts/login')
def lista_sesionesPOS(request):
    
    obj_sesiones=SesionPOS.objects.all().order_by('-pk')
    
    context={
        'sesiones':obj_sesiones
    }

    return render(request,'lista_sesionesPOS.html',context)

@login_required(login_url='/accounts/login')
def cerrar_sesion_pos(request):
    last_sesion = SesionPOS.objects.last()
    if last_sesion.fecha_cierre is not None:
        return alertas(request,'error','No hay ninguna sesion POS abierta.')
    
    obj_ventas=TicketsPOS.objects.filter(cierre=None,estado='Terminado')
    ventas=obj_ventas.aggregate(Sum('valor'))['valor__sum']
    if ventas is None: ventas=0
    
    obj_pagos=Pagos_Clientes.objects.filter(documento__cierre=None,documento__estado='Terminado',valor__gt=0)
    pagos=obj_pagos.aggregate(Sum('valor'))['valor__sum']
    if pagos is None: pagos=0
    
    por_cobrar=ventas-pagos
    
    obj_ajustes=AjustesCaja.objects.filter(cierre=None)
    ajustes=obj_ajustes.aggregate(Sum('valor'))['valor__sum']
    if ajustes is None: ajustes=0
    
    obj_cartera=Pagos_Clientes.objects.filter(cierre=None,valor__gt=0).exclude(documento__cierre=None)
    cartera=obj_cartera.aggregate(Sum('valor'))['valor__sum']
    if cartera is None: cartera=0
    
    obj_dev=Devoluciones.objects.filter(cierre=None)
    devoluciones=obj_dev.aggregate(Sum('valor'))['valor__sum']
    if devoluciones is None: devoluciones=0
    
    total_sesion=last_sesion.base+ventas-por_cobrar+ajustes+cartera+devoluciones
    
    context={
        'sesion':last_sesion.pk,
        'base':last_sesion.base,
        'ventas':ventas,
        'por_cobrar':por_cobrar,
        'ajustes':ajustes,
        'devoluciones':devoluciones,
        'cartera':cartera,
        'total_sesion':total_sesion,
    }
    
    if request.method == 'POST':
        last_sesion.fecha_cierre=datetime.datetime.now()
        last_sesion.usuario_cierre=str(request.user)
        last_sesion.ventas=ventas
        last_sesion.porcobrar=por_cobrar
        last_sesion.ajustes=ajustes
        last_sesion.devoluciones=devoluciones
        last_sesion.cartera_pagada=cartera
        last_sesion.efectivo_sesion=total_sesion
        last_sesion.save()
        
        for ticket in obj_ventas:
            ticket.cierre=last_sesion.pk
            ticket.save()
        for pago in obj_pagos:
            pago.cierre=last_sesion.pk
            pago.save()
        for abono in obj_cartera:
            abono.cierre=last_sesion.pk
            abono.save()
        for devolucion in obj_dev:
            devolucion.cierre=last_sesion.pk
            devolucion.save()
        for ajuste in obj_ajustes:
            ajuste.cierre=last_sesion.pk
            ajuste.save()
        accion=f'Cerro una sesión POS por ${total_sesion:,}'
        HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='POS',accion=accion)
        return HttpResponseRedirect('/ventas/sesionesPOS/todas')
    
    return render(request,'cierrePOS.html',context)

@login_required(login_url='/accounts/login')
def devolucion_ticket(request,ticket):
    last_sesion = SesionPOS.objects.last()
    if last_sesion.fecha_cierre is not None:
        return alertas(request,'error','No hay ninguna sesion POS abierta.')
    obj_ticket=TicketsPOS.objects.get(pk=ticket)
    detalle_productos=Ventas.objects.filter(docventa=ticket).values('producto','valor').annotate(Sum('cantidad'))
    detalle_productos=json.dumps(list(detalle_productos))
    pagos=Pagos_Clientes.objects.filter(documento=ticket).aggregate(Sum('valor'))
    pagos=pagos['valor__sum']
    
    context={
        'ticket':ticket,
        'obj_ticket':obj_ticket,
        'productos':detalle_productos,
        'pagado':pagos,
    }
    
    if request.method == 'POST':
        nroTicket = request.POST.get('nroTicket')
        obj_ticket=TicketsPOS.objects.get(pk=nroTicket)
        obj_cliente=Terceros.objects.get(identificacion=obj_ticket.cliente.pk)
        valor_devolucion=request.POST.get('totalCobro')
        dinero_devuelto=request.POST.get('dineroEntregado')
        print(dinero_devuelto)
        if dinero_devuelto=='': dinero_devuelto=0
        Devoluciones.objects.create(fecha=datetime.date.today(),cliente=obj_cliente,
                                    usuario=request.user,valor=valor_devolucion,ticket=obj_ticket)
        if int(dinero_devuelto)<0:
            Pagos_Clientes.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                        valor=dinero_devuelto,documento=obj_ticket)
        
        productos = request.POST.getlist('codigoDetalle')
        cantidades = request.POST.getlist('cantidadDetalle')
        valores = request.POST.getlist('precioDetalle')

        for i in range(0,len(productos)):
            producto=Productos.objects.get(pk=productos[i])
            Ventas.objects.create(fecha=datetime.date.today(),
                                    producto=producto,
                                    valor=valores[i],
                                    cantidad=cantidades[i],
                                    docventa=TicketsPOS.objects.get(pk=nroTicket))
        
        return HttpResponseRedirect('/ventas/tickets/todos')
        """ mensaje_alerta=f'Se aplicó devolucion sobre el ticket {nroTicket}'
        context['alerta']=True
        context['tipo_alerta']='success'
        context['mensaje_alerta']=mensaje_alerta """
         
    return render(request,'devolucion_ticket.html',context)

@login_required(login_url='/accounts/login')
def abono_cuenta(request):
    
    if request.method == 'POST':
        abonado=int(request.POST.get('abonado'))
        cliente=request.POST.get('cliente')
        
        tickets_pendientes = TicketsPOS.objects.raw(f'CALL lista_tickets("{cliente}")')
        for ticket in tickets_pendientes:
            if ticket.pendiente>0:
                valor_pendiente=ticket.pendiente
                if abonado>=valor_pendiente:
                   valor_pagado=valor_pendiente
                else:
                    valor_pagado=abonado
                Pagos_Clientes.objects.create(fecha=datetime.date.today(),
                                                usuario=request.user,
                                                valor=valor_pagado,
                                                documento=TicketsPOS.objects.get(pk=ticket.pk))
                abonado-=valor_pagado
                if abonado==0: break
        
        
        
    
    obj_clientes=TicketsPOS.objects.raw('CALL estados_cuenta("")')
    
    context={
        'clientes':obj_clientes,
    }
    
    
    return render(request,'abono_cuenta.html',context)

@login_required(login_url='/accounts/login')
def ajustes_caja(request):
    
    last_sesion = SesionPOS.objects.last()
    if last_sesion.fecha_cierre is not None:
        return alertas(request,'error','No hay ninguna sesion POS abierta.')
    context={
        
    }
    
    if request.method == 'POST':
        tipo=request.POST.get('tipo')
        valor=int(request.POST.get('valorAjuste'))
        descripcion=request.POST.get('descripcion')
        
        if tipo=='Credito':
            valor*=-1
        
        AjustesCaja.objects.create(tipo=tipo,fecha=datetime.date.today(),
                                   usuario=request.user,valor=valor,
                                   descripcion=descripcion)
        accion=f'Realizó un ajuste de caja por ${valor:,}'
        HistoryLine.objects.create(fecha=datetime.date.today(),usuario=request.user,
                                    modulo='POS',accion=accion)
        return HttpResponseRedirect('/welcome')
        
    
    return render(request,'modal_ajustesCaja.html',context)

def alertas(request,tipo,mensaje):
    """
    los tipos de error debe ser (error,warning,success)
    """
    context={
        'tipo':tipo,
        'mensaje':mensaje,
    }
    return render(request,'alertas/alertas_modal.html',context)

@login_required(login_url='/accounts/login')
def history_acciones(request):
    obj_history=HistoryLine.objects.all().reverse()
    context={
        'acciones':obj_history,
    }
    return render(request,'lista_history.html',context)

@login_required(login_url='/accounts/login')
def lista_productos_sesion(request,sesion):
    obj_productos=Ventas.objects.filter(docventa__cierre=sesion).select_related('producto')
    obj_productos=obj_productos.values('producto').annotate(cantidad=Sum('cantidad'),valor=Sum('valor'))
    for producto in obj_productos:
        try: nombre=Productos.objects.get(pk=producto['producto']).nombre
        except: nombre=''
        producto['nombre']=nombre
        print(producto)
    
    context={
        'productos':obj_productos,  
        'sesion':sesion,
    }
    return render(request,'lista_productosPOS.html',context)

@login_required(login_url='/accounts/login')
def lista_ajustes(request):
    obj_ajustes=AjustesCaja.objects.all().order_by('-pk')
    context={
        'ajustes':obj_ajustes
    }
    return render(request,'lista_ajustes.html',context)

@login_required(login_url='/accounts/login')
def lista_pagos_cartera(request):
    obj_abonos=Pagos_Clientes.objects.filter(fecha__gt=F('documento__fecha'))
    context={
        'pagos':obj_abonos,
    }
    
    return render(request,'lista_abonoscartera.html',context)

@login_required(login_url='/accounts/login')
def lista_productos_2(request):
    
    print(f'entra en {datetime.datetime.now()}')
    obj_productos=InfoProductos.objects.filter(estado='Activo')
    #obj_productos=Productos.objects.filter(estado='Activo')
    print(f'sale en {datetime.datetime.now()}')
    context={
        'productos':obj_productos
    }
    return render(request,'lista_productos.html',context)

#Auxiliares
def handler403(request, *args, **argv):
    context={}
    return render(request,'403.html',context) 

def check_perms(request,perms:list,raise_exception=True):
    user=request.user
    permissions=user.get_all_permissions()
    permissions_granted=0
    permissions_required=len(perms)
    for perm in perms:
        if perm in permissions:
            permissions_granted+=1
    if permissions_granted==permissions_required:
        return True
    if raise_exception:
        raise PermissionDenied
    return False
""" mensaje_alerta='La compra fue registrada con exito, recuerda solicitar su aprobacion para envio a cuentas por pagar'
context['alerta']=True
context['tipo_alerta']='success'
context['mensaje_alerta']=mensaje_alerta """