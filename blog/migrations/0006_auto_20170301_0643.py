# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 06:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170228_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'get_latest_by': 'publication_date', 'ordering': ['-publication_date'], 'permissions': (('can_view_all', 'Can view all entries'), ('can_change_status', 'Can change status'), ('can_change_author', 'Can change author(s)')), 'verbose_name': 'entry', 'verbose_name_plural': 'entries'},
        ),
        migrations.RenameField(
            model_name='entry',
            old_name='owner',
            new_name='author',
        ),
        migrations.AlterIndexTogether(
            name='entry',
            index_together=set([('status', 'publication_date'), ('start_publication', 'end_publication')]),
        ),
    ]
