from django import forms
from crispy_forms import bootstrap
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

from Sales.models import Terceros

class form_DatosProducto(forms.Form):
    Codigo = forms.CharField()
    Codigo.widget.attrs.update(id='codigo',readonly=True)
    Codigo.widget.attrs['class']='text-center'
    
    Stock = forms.IntegerField()
    Stock.widget.attrs['class']='text-center'
    Stock.widget.attrs.update(id='stock',readonly=True)
    
    Descripcion = forms.CharField()
    Descripcion.widget.attrs.update(id='descripcion')
    
    Nombre_Alterno = forms.CharField(required=False)
    Nombre_Alterno.widget.attrs.update(id='nombre_alterno')
    Nombre_Alterno.widget.attrs['class']='text-center'
    
    Codigo_Alterno = forms.CharField(required=False)
    Codigo_Alterno.widget.attrs.update(id='codigo_alterno')
    Codigo_Alterno.widget.attrs['class']='text-center'
    
    Marca = forms.CharField(required=False)
    Marca.widget.attrs.update(id='marca')
    Marca.widget.attrs['class']='text-center'
    
    Ubicacion = forms.CharField(required=False)
    Ubicacion.widget.attrs.update(id='ubicacion')
    Ubicacion.widget.attrs['class']='text-center'
    
    Precio = forms.IntegerField(min_value=0)
    Precio.widget.attrs.update(id='precio')
    Precio.widget.attrs['class']='text-center'

class form_NuevoProducto(forms.Form):
    Codigo = forms.CharField()
    Codigo.widget.attrs.update(id='codigoNuevo',readonly=True)
    Codigo.widget.attrs['class']='text-center'
    
    Descripcion = forms.CharField()
    placeholder = 'TIPO ARTICULO + MODELO MOTO + MEDIDA O TIPO + MARCA'
    Descripcion.widget.attrs.update(id='descripcionNuevo',placeholder=placeholder)
    
    Nombre_Alterno = forms.CharField(required=False)
    Nombre_Alterno.widget.attrs.update(id='nombre_alternoNuevo')
    
    Codigo_Alterno = forms.CharField(required=False)
    Codigo_Alterno.widget.attrs.update(id='codigo_alternoNuevo')
    Codigo_Alterno.widget.attrs['class']='text-center'
    
    Marca = forms.CharField(required=False)
    Marca.widget.attrs.update(id='marcaNuevo')
    Marca.widget.attrs['class']='text-center'

    Ubicacion = forms.CharField(required=False)
    Ubicacion.widget.attrs.update(id='ubicacionNuevo')
    Ubicacion.widget.attrs['class']='text-center'
    
    Precio = forms.IntegerField(min_value=0,required=False)
    Precio.widget.attrs.update(id='precioNuevo')
    Precio.widget.attrs['class']='text-center'

class form_AjustesInv(forms.Form):
    
    Codigo_ajuste = forms.CharField(label='Codigo')
    Codigo_ajuste.widget.attrs.update(id='codigoAjuste',readonly=True)
    Codigo_ajuste.widget.attrs['class']='text-center'
    
    Stock_ajuste = forms.IntegerField(label='Stock actual')
    Stock_ajuste.widget.attrs['class']='text-center'
    Stock_ajuste.widget.attrs.update(id='stockAjuste',readonly=True)
    
    Nuevo_Stock = forms.IntegerField(label='Nuevo stock',min_value=0)
    Nuevo_Stock.widget.attrs['class']='text-center'
    Nuevo_Stock.widget.attrs.update(id='nuevo_stock',readonly=True)
    
    tipos = (
        ('Debito','Debito'),
        ('Credito','Credito')
    )
    
    Tipo_ajuste=forms.ChoiceField(choices=tipos)
    Cantidad=forms.IntegerField(min_value=1)
    Cantidad.widget.attrs.update(id='cantidadAjuste')
    Cantidad.widget.attrs['class']='text-center'
    Cantidad.initial=0
    descripAjuste=forms.CharField(max_length=255,label='Descripcion')
    descripAjuste.widget.attrs.update(id='descripcionAjuste')
    
class form_Tercero(forms.Form):
    
    Identificacion = forms.CharField(max_length=255)
    Nombre = forms.CharField(max_length=255)
    Direccion = forms.CharField(max_length=255,required=False)
    Telefono_1 = forms.CharField(max_length=255,required=False,label='Celular')
    Telefono_2 = forms.CharField(max_length=255,required=False,label='Telefono')
    Tipo = forms.ChoiceField(choices=(
        ('Cliente','Cliente'),
        ('Proveedor','Proveedor')
    ))
    
class form_nuevaCompra(forms.Form):
     
    nroFactura = forms.CharField(label='Nro Factura')
    nroFactura.widget.attrs['class']='text-center'
    Fecha_Factura = forms.DateField(widget=DatePicker(
                                    options={
                                        'useCurrent': True,
                                        'collapse': False,
                                        'locale':'es',
                                        'format':'YYYY-MM-DD',
                                        
                                    },
                                    attrs={
                                        'class':'text-center',
                                        'append': 'fa fa-calendar',
                                        'icon_toggle': True,
                                    }),initial=datetime.datetime.today()) 
    
    
""" forms.DateField(label='Fecha de Nacimiento',widget=DatePicker(
                                    options={
                                        'useCurrent': True,
                                        'collapse': False,
                                        'format':'YYYY-MM-DD',
                                        
                                    },
                                    attrs={
                                        'append': 'fa fa-calendar',
                                        'icon_toggle': True,
                                    }),initial=datetime.datetime.today()) """