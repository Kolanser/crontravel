# Generated by Django 4.2.2 on 2023-07-06 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excursions', '0006_alter_application_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='company',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='excursion',
            name='slug',
        ),
    ]