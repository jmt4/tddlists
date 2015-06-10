# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AddField(
            model_name='item',
            name='text_hash',
            field=models.CharField(default='', blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(default='', max_length=256),
        ),
    ]
