"""intellySell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from Sales import views as Sales_views
from Sales import ajax_requests

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('ajax/',include(ajax_requests.urls)),
    path('',Sales_views.welcome),
    path('welcome',Sales_views.welcome,name='welcome'),
    path('productos/todos/<estado>',Sales_views.lista_productos,name='AllProductos'),
    path('datatables/kardex/<codigo_producto>',Sales_views.data_kardex,name='kardex'),
    path('terceros/nuevo',Sales_views.Nuevo_Tercero,name='Nuevo Tercero'),
    path('compras/nuevo',Sales_views.Nueva_Compra,name='Nueva compra'),
    path('compras/todas/<estado>',Sales_views.lista_compras,name='lista compras'),
    path('terceros/todos',Sales_views.lista_terceros,name='Lista Terceros'),
    path('compras/modificar/<proveedor>/<factura>',Sales_views.Modificar_Compra,name='Modificar Compra'),
    path('compras/transito',Sales_views.transito_compras,name='Transito compras'),
    path('ventas/pos/nuevo',Sales_views.pos,name='POS'),
    path('ventas/sesionesPOS/nueva',Sales_views.abrir_sesion_pos,name='Nueva Sesion POS'),
    path('ventas/sesionesPOS/cerrar',Sales_views.cerrar_sesion_pos,name='Cerrar Sesion POS'),
    path('ventas/tickets/todos',Sales_views.lista_tickets,name='Listado Tickets'),
    path('ventas/tickets/ver/<ticket>',Sales_views.ver_ticket,name='Ver Ticket'),
    path('ventas/tickets/devolucion/<ticket>',Sales_views.devolucion_ticket,name='Devolucion Ticket'),
    path('ventas/sesionesPOS/todas',Sales_views.lista_sesionesPOS,name='SesionesPOS'),
    path('ventas/sesionesPOS/ajustes',Sales_views.ajustes_caja,name='Ajustes Caja'),
    path('cartera/abono_cuenta',Sales_views.abono_cuenta,name='Abono a cuenta'),
    path('historyline',Sales_views.history_acciones,name='Historyline'),
    path('ventas/sesionesPOS/productos_vendidos/<sesion>',Sales_views.lista_productos_sesion),
    path('caja/ajustes/todos',Sales_views.lista_ajustes,name='Lista Ajustes'),
    path('cartera/abonos/todos',Sales_views.lista_pagos_cartera,name='Lista Abonos'),
    path('pruebas',Sales_views.lista_productos_2)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler403 = 'Sales.views.handler403'
