# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0004_auto_20151008_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='type',
            field=models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')]),
        ),
    ]
