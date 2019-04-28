# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u5956\u9879id', primary_key=True)),
                ('name', models.CharField(default=b'', max_length=50, verbose_name='\u5956\u9879\u540d\u5b57')),
                ('requirement', models.TextField(default=b'', verbose_name='\u8bc4\u5956\u6761\u4ef6')),
                ('organization', models.CharField(default=b'', max_length=20, verbose_name='\u6240\u5c5e\u7ec4\u7ec7')),
                ('has_extra_info', models.BooleanField(default=True, verbose_name='\u662f\u5426\u8981\u6c42\u4e0a\u4f20\u9644\u4ef6')),
                ('status', models.BooleanField(default=True, verbose_name='\u72b6\u6001')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u5220\u9664')),
                ('submit_start_time', models.DateTimeField(verbose_name='\u5f00\u59cb\u65e5\u671f')),
                ('submit_end_time', models.DateTimeField(verbose_name='\u7ed3\u675f\u65e5\u671f')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u5956\u9879',
                'verbose_name_plural': '\u5956\u9879',
            },
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u9879\u76ee\u7ea7\u522bid', primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u9879\u76ee\u7ea7\u522b')),
            ],
            options={
                'verbose_name': '\u9879\u76ee\u7ea7\u522b\u9009\u9879',
                'verbose_name_plural': '\u9879\u76ee\u7ea7\u522b\u9009\u9879',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u7533\u8bf7\u8868id', primary_key=True)),
                ('creator', models.CharField(default=b'', max_length=200, verbose_name='\u7533\u8bf7\u8005')),
                ('info', models.TextField(default=b'', verbose_name='\u4e8b\u8ff9\u4ecb\u7ecd')),
                ('extra_info', models.FileField(upload_to=b'', verbose_name='\u9644\u4ef6')),
                ('status', models.IntegerField(verbose_name='\u72b6\u6001', choices=[(0, '\u7533\u62a5\u4e2d'), (1, '\u672a\u901a\u8fc7'), (2, '\u5df2\u901a\u8fc7'), (3, '\u672a\u83b7\u5956'), (4, '\u5df2\u83b7\u5956')])),
                ('updater', models.CharField(default=b'', max_length=20, verbose_name='\u5ba1\u6279\u8005')),
                ('comment', models.TextField(verbose_name='\u8bc4\u8bed')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u5ba1\u6279\u65f6\u95f4')),
            ],
            options={
                'verbose_name': '\u7533\u8bf7\u8868',
                'verbose_name_plural': '\u7533\u8bf7\u8868',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u7ec4\u7ec7id', primary_key=True)),
                ('name', models.CharField(default=b'', max_length=20, verbose_name='\u7ec4\u7ec7\u540d\u79f0')),
                ('principal', models.CharField(default=b'', max_length=20, verbose_name='\u8d1f\u8d23\u4eba')),
                ('users', models.TextField(verbose_name='\u7528\u6237')),
                ('is_delete', models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u5220\u9664')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('updater', models.ForeignKey(verbose_name='\u66f4\u65b0\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7ec4\u7ec7',
                'verbose_name_plural': '\u7ec4\u7ec7',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u7528\u6237\u6743\u9650id', primary_key=True)),
                ('name', models.CharField(default=b'', max_length=20, verbose_name='\u7528\u6237\u6743\u9650\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u7528\u6237QQ\u4fe1\u606fid', primary_key=True)),
                ('auth_token', models.CharField(default=b'', max_length=255, verbose_name='\u7528\u6237openId', blank=True)),
                ('qq', models.CharField(default=b'', max_length=20, verbose_name='\u7528\u6237QQ')),
            ],
            options={
                'verbose_name': '\u7528\u6237QQ\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237QQ\u4fe1\u606f',
            },
        ),
        migrations.CreateModel(
            name='UserPermission',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='\u7528\u6237\u6743\u9650code id', primary_key=True)),
                ('qq', models.CharField(default=b'', max_length=20, verbose_name='\u7528\u6237QQ')),
                ('permission', models.ForeignKey(verbose_name='\u7528\u6237\u6743\u9650', to='home_application.Permission')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6743\u9650code',
                'verbose_name_plural': '\u7528\u6237\u6743\u9650code',
            },
        ),
        migrations.AddField(
            model_name='award',
            name='level',
            field=models.ForeignKey(verbose_name='\u9879\u76ee\u7ea7\u522b', to='home_application.Choice'),
        ),
    ]
