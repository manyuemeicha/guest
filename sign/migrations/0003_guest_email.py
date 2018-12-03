# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0002_auto_20181122_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='email',
            field=models.EmailField(max_length=254, default=2),
            preserve_default=False,
        ),
    ]
