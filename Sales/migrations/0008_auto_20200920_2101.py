# Generated by Django 3.0.5 on 2020-09-21 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0007_auto_20200920_1825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ajustesinventario',
            old_name='creditos',
            new_name='cantidad',
        ),
        migrations.RemoveField(
            model_name='ajustesinventario',
            name='debitos',
        ),
    ]
