# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sucursales', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo_precio', models.CharField(max_length=20)),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_real', models.FloatField()),
                ('precio', models.FloatField()),
                ('descripcion', models.CharField(max_length=50, blank=True)),
                ('importe', models.FloatField(default=0.0)),
                ('detalle_Sucursal_almacen_id', models.ForeignKey(to='sucursales.DetalleSucursalAlmacen')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha_emision', models.DateTimeField(auto_now=True)),
                ('referencia', models.TextField(unique=True, null=True)),
                ('nombre_ventas_descripcion', models.CharField(default=b'NEW', max_length=20, choices=[(b'NUE', b'Nueva'), (b'MOD', b'modificada'), (b'ELI', b'modificada')])),
                ('estado', models.BooleanField(default=True)),
                ('total', models.FloatField(default=0.0, blank=True)),
                ('empleado', models.ForeignKey(to='sucursales.SucursalTrabajador')),
                ('sucursal', models.ForeignKey(to='sucursales.Sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='detalleventa',
            name='venta_id',
            field=models.ForeignKey(to='ventas.Venta'),
        ),
    ]
