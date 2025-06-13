from app.models import Report
from django.http import HttpResponse
from django.shortcuts import render

from excel_extract.excel import Excel


def index(request):
    return render(request, 'index.html', {})


def extract_excel_get(request):
    queryset = Report.objects.get(id=1)

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_get',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    return excel.to_excel()


def extract_excel_filter(request):
    queryset = Report.objects.filter(id=1)

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_filter',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    return excel.to_excel()


def extract_excel_values(request):
    queryset = Report.objects.values(
        'id', 'report_num', 'status_report', 'type_report', 'priority'
    )

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_values',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    return excel.to_excel()


def extract_excel_values_list(request):
    queryset = Report.objects.values_list(
        'report_num', 'status_report', 'type_report', 'priority'
    )

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_values_list',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    print(excel.get_data_frame())

    return HttpResponse('Test')
    # return excel.to_excel()
