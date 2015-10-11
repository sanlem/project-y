# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0004_auto_20151008_1618'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='petitionsign',
            unique_together=set([('author', 'petition')]),
        ),
    ]
