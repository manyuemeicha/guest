# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='name',
            new_name='realname',
        ),
        migrations.RenameField(
            model_name='guest',
            old_name='status',
            new_name='sign',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='email',
        ),
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(verbose_name='event time'),
        ),
    ]
