# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0003_media'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='url',
            new_name='mediaUrl',
        ),
    ]
