from django.http import HttpResponse
from django.shortcuts import render

from app.models import Report, StatusReport, TypeReport, Priority
from excel_extract.excel import Excel
from django.db.models import ExpressionWrapper, F, DurationField
from django.db.models.functions import Now


def index(request):
    return render(request, 'index.html', {})


def extract_excel(request):
    # queryset = Report.objects.values('priority', 'type_report')
    queryset = Report.objects.get(id=1)
    # queryset = Report.objects.filter(id=1)
    # queryset = Report.objects.values(
    #     'id', 'report_num', 'status_report', 'type_report', 'priority'
    # )

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    # excel.get_data_frame()

    # return HttpResponse('Test')

    return excel.to_excel()
