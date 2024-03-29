# Generated by Django 3.0.5 on 2020-09-20 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0004_remove_productos_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('idCompra', models.AutoField(primary_key=True, serialize=False)),
                ('producto', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('valor', models.IntegerField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, max_length=255, null=True)),
                ('doccompra', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Compras_General',
            fields=[
                ('idCompra', models.AutoField(primary_key=True, serialize=False)),
                ('nroFactura', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('valor', models.IntegerField(blank=True, null=True)),
                ('usuario', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'managed': True,
                'unique_together': {('nroFactura', 'proveedor')},
            },
        ),
    ]
