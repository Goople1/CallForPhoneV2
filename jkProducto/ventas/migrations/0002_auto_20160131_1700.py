# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='nombre_ventas_descripcion',
            field=models.CharField(max_length=20, choices=[(b'NUE', b'Nueva'), (b'MOD', b'modificada'), (b'ELI', b'modificada')]),
        ),
    ]
