# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0003_petitionsign'),
    ]

    operations = [
        migrations.RenameField(
            model_name='petitionsign',
            old_name='user',
            new_name='author',
        ),
    ]
