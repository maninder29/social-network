# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 18:37
from __future__ import unicode_literals

from django.db import migrations, models
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_like_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=posts.models.profile_pic_upload),
        ),
    ]
