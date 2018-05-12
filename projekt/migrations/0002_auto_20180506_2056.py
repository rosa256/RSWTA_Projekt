# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-06 18:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projekt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imie', models.CharField(max_length=100)),
                ('wiek', models.IntegerField()),
                ('wyksztalcenie', models.CharField(max_length=100)),
                ('pochodzenie', models.CharField(max_length=100)),
                ('telefon', models.CharField(blank=True, default='', max_length=20)),
                ('miasto', models.CharField(blank=True, default='', max_length=100)),
                ('panstwo', models.CharField(blank=True, default='', max_length=100)),
                ('opis', models.TextField(blank=True, default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Aplikant',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]