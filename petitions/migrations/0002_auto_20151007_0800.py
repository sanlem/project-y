# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petition',
            name='responsible',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
