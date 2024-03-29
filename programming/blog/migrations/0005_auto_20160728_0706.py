# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 07:06
from __future__ import unicode_literals

import blog.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(help_text='Markdown 문법을 써주세요.', validators=[blog.validators.MinLengthValidator(10)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, validators=[blog.validators.MinLengthValidator(4)], verbose_name='제목'),
        ),
    ]
