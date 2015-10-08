# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('petitions', '0002_auto_20151007_0800'),
    ]

    operations = [
        migrations.CreateModel(
            name='PetitionSign',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('comment', models.TextField(blank=True, max_length=200, null=True)),
                ('anonymous', models.BooleanField(default=False)),
                ('petition', models.ForeignKey(to='petitions.Petition', related_name='signs')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='signed')),
            ],
        ),
    ]
