# Generated by Django 3.0.5 on 2020-09-20 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sales', '0003_historyline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productos',
            name='stock',
        ),
    ]
