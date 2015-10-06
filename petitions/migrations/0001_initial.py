# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(default='V', choices=[('V', 'Voting'), ('A', 'Accepted'), ('D', 'Declined')], max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='petitions')),
                ('responsible', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='responsible')),
            ],
        ),
    ]
