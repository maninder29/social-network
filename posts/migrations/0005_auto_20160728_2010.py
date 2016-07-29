# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-28 20:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import posts.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0004_post_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to=posts.models.profile_pic_upload)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.TextField(blank=True, null=True)),
                ('phone', models.CharField(max_length=10)),
                ('dob', models.DateField()),
                ('relationship_status', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='profile_pic',
        ),
    ]
