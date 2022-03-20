from statistics import mode
from tabnanny import verbose
from time import time
from django import forms
from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL(slug)")
    brief = models.TextField(blank=False, verbose_name="Краткое описание")
    content = models.TextField(blank=False, verbose_name="Контент")
    photo = models.ImageField(
        upload_to='photos/%Y-%m-%d', verbose_name="Фото", blank=True)
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('new', kwargs={'new_slug': self.slug})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['time_create', 'title']


class GVS(models.Model):
    street = models.CharField(verbose_name='Улица', max_length=50)
    build = models.CharField(verbose_name='Дом', max_length=50)
    REGIONS = (
        ('Северный сетевой район', 'Северный сетевой район'),
        ('Южный сетевой район', 'Южный сетевой район'),
    )
    region = models.CharField(
        verbose_name='Сетевой район', max_length=50, choices=REGIONS)
    date_disconnect = models.DateField(verbose_name="Дата отключения")
    date_connect = models.DateField(
        verbose_name="Ориентировочная дата устранения")
    reason = models.CharField(
        verbose_name='Причина отсутствия ГВС', max_length=250)

    def __str__(self):
        return f'{self.region} {self.street} {self.build}'

    class Meta:
        verbose_name = 'Элемент списка'
        verbose_name_plural = 'Список домов Северного и Южного сетевых районов, в которых отсутствует ГВС'
        ordering = ['id', 'region', 'street', 'build']
