# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('username', models.CharField(serialize=False, primary_key=True, max_length=16)),
                ('password', models.CharField(max_length=16)),
                ('following', models.ManyToManyField(to='social.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('age', models.IntegerField()),
                ('sex', models.CharField(verbose_name='sex', max_length=1, choices=[('M', 'Male'), ('F', 'Female')])),
                ('like', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ('created',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('text', models.CharField(max_length=4096)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='messages',
            field=models.OneToOneField(to='social.Message', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='profile',
            field=models.OneToOneField(to='social.Profile', null=True),
            preserve_default=True,
        ),
    ]
