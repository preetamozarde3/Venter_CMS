# Generated by Django 2.1.2 on 2019-07-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venter', '0040_auto_20190627_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='domain_present',
            field=models.BooleanField(default=False),
        ),
    ]