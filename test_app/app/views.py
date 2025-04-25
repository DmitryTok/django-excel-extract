from django.shortcuts import render

from app.models import Report, StatusReport, Priority, TypeReport
from excel_extract.excel import Excel
import sys
import os


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
)


def index(request):
    return render(request, 'index.html', {})


def extract_excel(request):
    queryset = Report.objects.all()
    exclude = ['id']
    choices = {
        'status_report': {item.name: item.value for item in StatusReport},
        'type_report': {item.name: item.value for item in TypeReport},
    }

    excel = Excel(
        model=Report,
        queryset=queryset,
        choices=choices,
        file_name='report',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y %H:%M',
    )

    return excel.to_excel()
