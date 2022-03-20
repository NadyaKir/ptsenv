import csv
import datetime
from django.contrib import admin
from django.utils.safestring import mark_safe
from openpyxl import Workbook
from .models import *
from rangefilter.filters import DateRangeFilter
from import_export.admin import ExportActionModelAdmin
from .resources import GVSResource
from django.http import HttpResponse
from django.core import serializers
from django.http import HttpResponse
import xlwt
from datetime import date


@admin.action(description='Отметить выбранные новости как неопубликованные')
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.action(description='Отметить выбранные новости как опубликованные')
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create',
                    'get_html_photo', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'brief', 'content')
    list_editable = ('is_published',)
    prepopulated_fields = {"slug": ("title",)}
    fields = ('title', 'slug', 'brief', 'content', 'photo', 'get_html_photo',
              'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    list_filter = ('is_published', ('time_create', DateRangeFilter), ('time_update', DateRangeFilter),
                   )
    date_hierarchy = 'time_create'
    actions = [make_unpublished, make_published]

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=100")

    get_html_photo.short_description = "Миниатюра"

    def get_rangefilter_time_create_default(self, request):
        return (datetime.date.today, datetime.date.today)

    def get_rangefilter_time_update_default(self, request):
        return (datetime.date.today, datetime.date.today)


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GVSFullList_' + \
        str(date.today())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Список домов на ' + str(date.today()))

    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.height = 280
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_style.font.name = 'Times New Roman'

    ws.write_merge(
        1, 1, 2, 8, "Список жилых домов, в которых отсуствует ГВС на " + str(date.today()), font_style)

    row_num = 5
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    font_style.font.height = 240
    font_style.borders.top = 2
    font_style.borders.right = 2
    font_style.borders.left = 2
    font_style.borders.bottom = 2
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER

    columns = ['№', 'Сетевой район', 'Улица', 'Дом', 'Дата отключения',
               'Ориентир. дата устранения', 'Причина']

    ws.col(2).width = 1500  # №
    ws.col(3).width = 8000  # Сетевой район
    ws.col(4).width = 8000  # Улица
    ws.col(5).width = 4000  # Дом
    ws.col(6).width = 8000  # Дата отключения
    ws.col(7).width = 12000  # Ориентир. дата подключения
    ws.col(8).width = 50000  # Причина

    for col_num in range(len(columns)):
        ws.write(row_num, col_num + 2, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    font_style.font.height = 240
    font_style.borders.top = 1
    font_style.borders.right = 1
    font_style.borders.left = 1
    font_style.borders.bottom = 1
    font_style.font.name = 'Times New Roman'
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER

    rows = GVS.objects.all().values_list('id', 'region', 'street', 'build',
                                         'date_disconnect', 'date_connect', 'reason')

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num + 2, str(row[col_num]), font_style)
    wb.save(response)

    return response


export_excel.short_description = u"Export XLS"


def export_xls(modeladmin, request, queryset):

    import xlwt
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GVSFullList_' + \
        str(date.today())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Список домов на ' + str(date.today()))

    font_style = xlwt.XFStyle()
    font_style.font.height = 300
    font_style.font.bold = True
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_style.alignment.vert = xlwt.Alignment.VERT_CENTER
    font_style.font.name = 'Times New Roman'
    font_style.borders.top = 1
    font_style.borders.right = 1
    font_style.borders.left = 1
    font_style.borders.bottom = 1
    alignment = xlwt.Alignment()
    alignment.vert = 0x01
    alignment.horz = 0x01

    ws.write_merge(
        0, 0, 0, 6, "Список жилых домов, в которых отсуствует ГВС на " + str(date.today()), font_style)

    row_num = 1

    columns = [
        (u"№", 1500),
        (u"Сетевой район", 8000),
        (u"Улица", 8000),
        (u"Дом", 4000),
        (u"Дата отключения", 8000),
        (u"Ориентир. дата устранения", 12000),
        (u"Причина", 50000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.font.bold = True
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_style.alignment.vert = xlwt.Alignment.VERT_CENTER
    font_style.font.name = 'Times New Roman'
    font_style.borders.top = 1
    font_style.borders.right = 1
    font_style.borders.left = 1
    font_style.borders.bottom = 1
    alignment = xlwt.Alignment()
    alignment.vert = 0x01
    alignment.horz = 0x01

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.font.height = 280
    font_style.alignment.wrap = 1
    font_style.alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_style.alignment.vert = xlwt.Alignment.VERT_CENTER
    font_style.font.name = 'Times New Roman'
    font_style.borders.top = 1
    font_style.borders.right = 1
    font_style.borders.left = 1
    font_style.borders.bottom = 1
    alignment = xlwt.Alignment()
    alignment.vert = 0x01
    alignment.horz = 0x01

    for obj in queryset:
        row_num += 1
        row = [
            obj.pk,
            obj.region,
            obj.street,
            obj.build,
            obj.date_disconnect,
            obj.date_connect,
            obj.reason,
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)
    return response


export_xls.short_description = u"Экспортировать в Excel (.xls)"


class GVSAdmin(admin.ModelAdmin):

    list_display = ('id', 'region', 'street', 'build',
                    'date_disconnect', 'date_connect', 'reason')
    search_fields = ('region', '^street', '^build',
                     'date_disconnect', 'date_connect')
    list_editable = ('date_connect', 'reason')
    list_filter = ('region', 'reason', ('date_disconnect', DateRangeFilter),
                   ('date_connect', DateRangeFilter),)
    date_hierarchy = 'date_disconnect'
    actions = [export_xls, ]

    # resource_class = GVSResource

    def get_rangefilter_date_disconnect_default(self, request):
        return (datetime.date.today, datetime.date.today)

    def get_rangefilter_date_connect_default(self, request):
        return (datetime.date.today, datetime.date.today)


admin.site.empty_value_display = 'Пусто'

admin.site.register(News, NewsAdmin)
admin.site.register(GVS, GVSAdmin)

admin.site.site_title = 'Админ-панель ТОО "ПТС"'
admin.site.site_header = 'Админ-панель ТОО "ПТС"'
