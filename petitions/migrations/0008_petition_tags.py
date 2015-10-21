# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0007_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='petition',
            name='tags',
            field=models.ManyToManyField(to='petitions.Tag'),
        ),
    ]
