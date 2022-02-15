from django.db import models
from django.db.models import Avg, Max, Min, Sum

# Create your models here.


class Productos(models.Model):
    
    codigo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255,null=True,blank=True)
    nombrealterno = models.CharField(max_length=255,null=True,blank=True)
    codigoalterno = models.CharField(max_length=255,null=True,blank=True)
    marca = models.CharField(max_length=255,null=True,blank=True)
    ubicacion = models.CharField(max_length=255,null=True,blank=True)
    fechacreacion = models.DateField(null=True,blank=True)
    estado = models.CharField(max_length=255,null=True,blank=True)
    precio = models.IntegerField(blank=True,null=True)
    

class Terceros(models.Model):
    
    identificacion = models.CharField(max_length=255,primary_key=True)
    nombre = models.CharField(max_length=255,null=True,blank=True)
    direccion = models.CharField(max_length=255,null=True,blank=True)
    telefono = models.CharField(max_length=255,null=True,blank=True)
    celular = models.CharField(max_length=255,null=True,blank=True)
    tipo = models.CharField(max_length=255,null=True,blank=True)
    estado = models.CharField(max_length=255,null=True,blank=True)

class TicketsPOS(models.Model):
    
    idTicket = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True,null=True)
    cliente = models.ForeignKey(Terceros,on_delete=models.CASCADE)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    valor = models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=255,null=True,blank=True)
    cierre = models.CharField(max_length=255,null=True,blank=True)
    
class Ventas(models.Model):
    
    idVenta = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Productos,on_delete=models.CASCADE)
    fecha = models.DateField(blank=True,null=True)
    cantidad = models.IntegerField(blank=True,null=True)
    valor = models.IntegerField(blank=True,null=True)
    docventa = models.ForeignKey(TicketsPOS,on_delete=models.CASCADE)

class Compras_General(models.Model):
    
    idCompra = models.AutoField(primary_key=True)
    nroFactura = models.CharField(max_length=255,null=True,blank=True)
    proveedor =models.ForeignKey(Terceros,on_delete=models.CASCADE,max_length=255)
    fecha = models.DateField(blank=True,null=True)
    valor= models.IntegerField(blank=True,null=True)
    estado = models.CharField(max_length=255,null=True,blank=True)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    
    class Meta:
        managed = True
        unique_together = (('nroFactura', 'proveedor'),)
   

class Compras(models.Model):
    
    idCompra = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Productos,on_delete=models.CASCADE)
    fecha = models.DateField(blank=True,null=True)
    cantidad = models.IntegerField(blank=True,null=True)
    valor = models.IntegerField(blank=True,null=True)
    doccompra = models.ForeignKey(Compras_General,on_delete=models.CASCADE)

class Consecutivos(models.Model):
    
    tipo = models.CharField(max_length=255,null=True,blank=True)
    prefijo = models.CharField(max_length=255,null=True,blank=True)
    consecutivo = models.IntegerField(blank=True,null=True)
    
class AjustesCaja(models.Model):
    
    idAjuste = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True,null=True)
    tipo = models.CharField(max_length=255,null=True,blank=True)
    valor = models.IntegerField(blank=True,null=True)
    descripcion = models.CharField(max_length=255,null=True,blank=True)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    cierre = models.CharField(max_length=255,null=True,blank=True)
    
class AjustesInventario(models.Model):
    
    idAjuste = models.AutoField(primary_key=True)
    prod_ajuste = models.ForeignKey(Productos,null=True,blank=True,on_delete=models.CASCADE)
    producto = models.CharField(max_length=255,null=True,blank=True)
    concepto = models.CharField(max_length=255,null=True,blank=True)
    cantidad = models.IntegerField(blank=True,null=True)
    fecha = models.DateField(blank=True,null=True)
    usuario = models.CharField(max_length=255,null=True,blank=True)

class SesionPOS(models.Model):
    
    idSesion = models.AutoField(primary_key=True)
    fecha_apertura = models.DateTimeField(blank=True,null=True)
    fecha_cierre = models.DateTimeField(blank=True,null=True)
    usuario_apertura = models.CharField(max_length=255,null=True,blank=True)
    usuario_cierre = models.CharField(max_length=255,null=True,blank=True)
    base = models.IntegerField(blank=True,null=True)
    ventas = models.IntegerField(blank=True,null=True)
    porcobrar = models.IntegerField(blank=True,null=True)
    ajustes = models.IntegerField(blank=True,null=True)
    devoluciones = models.IntegerField(blank=True,null=True)
    pagos_efectuados = models.IntegerField(blank=True,null=True)
    cartera_pagada = models.IntegerField(blank=True,null=True)
    efectivo_sesion = models.IntegerField(blank=True,null=True)
    
class Pagos_Clientes(models.Model):
    
    idPago = models.AutoField(primary_key=True)
    documento = models.ForeignKey(TicketsPOS,on_delete=models.CASCADE)
    valor = models.IntegerField(blank=True,null=True)
    fecha = models.DateField(blank=True,null=True)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    cierre = models.CharField(max_length=255,null=True,blank=True)
    
class HistoryLine(models.Model):
    
    idmove = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True,null=True)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    modulo = models.CharField(max_length=255,null=True,blank=True)
    accion = models.CharField(max_length=255,null=True,blank=True)
    
class Devoluciones(models.Model):
    
    idDevolucion = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True,null=True)
    cliente = models.ForeignKey(Terceros,on_delete=models.CASCADE)
    usuario = models.CharField(max_length=255,null=True,blank=True)
    valor = models.IntegerField(blank=True,null=True)
    ticket = models.ForeignKey(TicketsPOS,on_delete=models.CASCADE)
    cierre = models.CharField(max_length=255,null=True,blank=True)

#Vistas
class InfoProductos(models.Model):
    producto = models.CharField(max_length=255,primary_key=True,db_column="codigo")
    nombre = models.CharField(max_length=255,db_column="nombre")
    codigoalterno = models.CharField(max_length=255,db_column="codigoalterno")
    nombrealterno = models.CharField(max_length=255,db_column="nombrealterno")
    marca = models.CharField(max_length=255,db_column="marca")
    precio = models.IntegerField(null=True,blank=True,db_column="precio")
    costo_promedio = models.IntegerField(null=True,blank=True,db_column="costo_promedio")
    costo_maximo = models.IntegerField(null=True,blank=True,db_column="costo_maximo")
    costo_minimo = models.IntegerField(null=True,blank=True,db_column="costo_minimo")
    stock = models.IntegerField(null=True,blank=True,db_column="stock")
    estado = models.CharField(max_length=255,db_column="estado")
    ubicacion = models.CharField(max_length=255,db_column="ubicacion")

    class Meta:

        managed = False
        db_table = "stock"

#Proxys

class ProxyTickets(TicketsPOS):
    class Meta:
        proxy = True
    
    def pagado(self):
        vrpagado=Pagos_Clientes.objects.filter(documento=self.pk).aggregate(Sum('valor'))
        vrpagado=vrpagado['valor__sum']
        if vrpagado is None: vrpagado=0
        return vrpagado
    
    def devolucion(self):
        vrdevuelto=Devoluciones.objects.filter(ticket=self.pk).aggregate(Sum('valor'))
        vrdevuelto=vrdevuelto['valor__sum']
        if vrdevuelto is None: vrdevuelto=0
        return vrdevuelto
        
    def pendiente(self):
        vrpagado=self.pagado()
        vrdevolucion=self.devolucion()
        pendiente = self.valor+vrdevolucion-vrpagado
        return pendiente
        
""" 
class InfoProductos(Productos):
    class Meta:
        proxy=True
    
    def codigo(self):
        return self.pk
    
    def nombre(self):
        return self.nombre
    
    def marca(self):
        return self.marca
    
    def precio(self):
        return self.precio
    
    def costo_promedio(self):
        compras = Compras.objects.filter(producto=self.pk)
        sup=0
        inf=0
        for compra in compras:
            sup+=compra.cantidad*compra.valor
            inf+=compra.cantidad
        try:
            promedio_ponderado=sup/inf
        except:
            promedio_ponderado=0
        return promedio_ponderado
    
    def costo_maximo(self):
        try:
            compras = Compras.objects.filter(producto=self.pk).aggregate(Max('valor'))
            costo_max = compras['valor__max']
        except:
            costo_max=0
        return costo_max
    
    def costo_minimo(self): 
        try:
            compras = Compras.objects.filter(producto=self.pk).aggregate(Min('valor'))
            costo_min = compras['valor__min']
        except:
            costo_min=0
        return costo_min

    def stock(self):
        
        compras = Compras.objects.filter(producto=self.pk)
        if compras.exists():
            compras=compras.aggregate(Sum('cantidad'))
            compras = compras['cantidad__sum']
        else:
            compras=0

        ventas = Ventas.objects.filter(producto=self.pk)
        if ventas.exists():
            ventas=ventas.aggregate(Sum('cantidad'))
            ventas=ventas['cantidad__sum']
        else:
            ventas=0
        
        ajustes=AjustesInventario.objects.filter(producto=self.pk)
        if ajustes.exists():
            ajustes=ajustes.aggregate(Sum('cantidad'))
            ajustes=ajustes['cantidad__sum']
        else:
            ajustes=0
        
        en_stock = compras+ajustes-ventas

        return en_stock
  """       
        


    

    


