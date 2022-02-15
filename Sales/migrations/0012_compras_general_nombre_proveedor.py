# Generated by Django 3.0.5 on 2020-09-27 01:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0011_compras_general_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='compras_general',
            name='nombre_proveedor',
            field=models.ForeignKey(default='null', on_delete=django.db.models.deletion.CASCADE, to='Sales.Terceros'),
            preserve_default=False,
        ),
    ]