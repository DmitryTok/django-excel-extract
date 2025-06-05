from django.shortcuts import render

from app.models import Report, StatusReport, TypeReport
from excel_extract.excel import Excel


def index(request):
    return render(request, 'index.html', {})


def extract_excel(request):
    queryset = Report.objects.all()
    # queryset = Report.objects.get(id=1)
    # queryset = Report.objects.filter(id=1)
    # queryset = Report.objects.values(
    #     'id', 'report_num', 'status_report', 'type_report'
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

    return excel.to_excel()
