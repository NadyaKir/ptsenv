# Generated by Django 3.2.7 on 2022-01-26 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y-%m-%d', verbose_name='Фото'),
        ),
    ]