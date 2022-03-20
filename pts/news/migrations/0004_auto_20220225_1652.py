# Generated by Django 3.2.7 on 2022-02-25 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_gsv'),
    ]

    operations = [
        migrations.CreateModel(
            name='GVS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50, verbose_name='Улица')),
                ('build', models.CharField(max_length=50, verbose_name='Дом')),
                ('region', models.CharField(max_length=50, verbose_name='Сетевой район')),
                ('date_disconnect', models.DateTimeField(verbose_name='Дата отключения')),
                ('date_connect', models.DateTimeField(verbose_name='Ориентировочная дата устранения')),
                ('reason', models.CharField(max_length=250, verbose_name='Причина отсутствия ГВС')),
            ],
        ),
        migrations.DeleteModel(
            name='GSV',
        ),
    ]