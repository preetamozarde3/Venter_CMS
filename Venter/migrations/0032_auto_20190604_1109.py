# Generated by Django 2.1.2 on 2019-06-04 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Venter', '0031_auto_20190516_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='output_file_json',
            field=models.FileField(blank=True, max_length=255, upload_to=''),
        ),
        migrations.AlterField(
            model_name='file',
            name='output_file_xlsx',
            field=models.FileField(blank=True, max_length=255, upload_to=''),
        ),
    ]
