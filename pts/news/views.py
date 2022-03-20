from msilib.schema import ListView
from pickle import TRUE
import re
from urllib import response
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from .resources import GVSResource
from .models import *
from django.core.paginator import Paginator
from .filters import FindGVSItem
import xlwt
from datetime import date


def index(request):
    last_news = News.objects.filter(
        is_published=True).order_by("-time_create")[0:3]

    results = GVS.objects.values_list(
        'street', flat=True).order_by('street').distinct()

    result = GVS.objects.all()
    myFilter = FindGVSItem(request.GET, queryset=result)
    result = myFilter.qs

    context = {
        'last_news': last_news,
        'results': results,
        'title': 'ТОО "Павлодарские тепловые сети"',
        'results_list': result,
        'myFilter': myFilter
    }

    return render(request, 'news/index.html', context)


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


def news(request):
    news_items = News.objects.filter(
        is_published=True).order_by("-time_create")

    paginator = Paginator(news_items, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Новости',
        'page_obj': page_obj,
    }

    return render(request, 'news/news.html', context)


def show_new(request, new_slug):
    new = get_object_or_404(News, slug=new_slug)

    context = {
        'new': new,
        'title': new.title,
    }

    return render(request, 'news/new.html', context=context)


def tariffs(request):

    context = {
        'title': 'Тарифы',
    }
    return render(request, 'news/tariff.html', context)


def contacts(request):

    context = {
        'title': 'Контакты',
    }

    return render(request, 'news/contacts.html', context)


def about(request):

    context = {
        'title': 'Общая информация',
    }

    return render(request, 'news/about.html', context)


def director(request):

    context = {
        'title': 'Руководитель',
    }

    return render(request, 'news/director.html', context)


def requisites(request):

    context = {
        'title': 'Реквизиты',
    }

    return render(request, 'news/requisites.html', context)


def consumerinfo(request):
    context = {
        'title': 'Потребителям',
    }

    return render(request, 'news/consumerinfo.html', context)


def sitemap(request):
    context = {
        'title': 'Карта сайта',
    }

    return render(request, 'news/sitemap.html', context)


def pageNotFound(request, exception):
    return render(request, 'news/404.html', status=404)


def search(request):

    if request.method == "POST":
        searched = request.POST['q']
        news_list = News.objects.raw('SELECT * FROM news_news WHERE title iLIKE %s OR brief iLIKE %s OR content iLIKE %s', [
            '%'+searched+'%', '%'+searched+'%', '%'+searched+'%'])

    paginator = Paginator(news_list, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/search.html',  {'searched':  searched, 'title': 'Результаты поиска',  'page_obj': page_obj, })
