# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HangupsApiUser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('user_id', models.CharField(max_length=200)),
                ('token', models.CharField(max_length=200)),
                ('memo', models.CharField(max_length=200)),
            ],
        ),
    ]
