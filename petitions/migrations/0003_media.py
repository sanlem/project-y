# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petitions', '0002_auto_20151007_0800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('url', models.URLField()),
                ('type', models.CharField(choices=[(('image', 'Image'), ('video', 'Video'))], max_length=10)),
                ('petition', models.ForeignKey(related_name='media', to='petitions.Petition')),
            ],
        ),
    ]
