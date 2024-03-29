# Generated by Django 3.0.5 on 2020-10-08 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0020_auto_20201003_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='SesionPOS',
            fields=[
                ('idSesion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_apertura', models.DateTimeField(blank=True, null=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('usuario_apertura', models.CharField(blank=True, max_length=255, null=True)),
                ('usuario_cierre', models.CharField(blank=True, max_length=255, null=True)),
                ('base', models.IntegerField(blank=True, null=True)),
                ('ventas', models.IntegerField(blank=True, null=True)),
                ('porcobrar', models.IntegerField(blank=True, null=True)),
                ('ajustes', models.IntegerField(blank=True, null=True)),
                ('devoluciones', models.IntegerField(blank=True, null=True)),
                ('pagos_efectuados', models.IntegerField(blank=True, null=True)),
                ('cartera_pagada', models.IntegerField(blank=True, null=True)),
                ('efectivo_sesion', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CierresPOS',
        ),
    ]
