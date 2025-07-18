from app.models import Priority, Report
from django.db.models import ExpressionWrapper, F, fields
from django.shortcuts import render
from django.utils.timezone import now

from excel_extract.excel import Excel


def index(request):
    return render(request, 'index.html', {})


def extract_excel_get(request):
    queryset = Report.objects.select_related('category').prefetch_related(
        'tag'
    )

    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_get',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y',
    )

    response = excel.to_excel()

    return response


def extract_excel_filter(request):
    queryset = Report.objects.filter(priority=Priority.HIGH)

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
    queryset = Report.objects.annotate(
        days_passed=ExpressionWrapper(
            now() - F('created_at'),
            output_field=fields.DurationField(),
        )
    ).values(
        'report_num',
        'status_report',
        'type_report',
        'priority',
        'days_passed',
    )

    aggregation_field_names = {'days_passed': 'Days Passed'}

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report_values',
        title='Report',
        date_time_format='%d/%m/%Y',
        annotation_fields_map=aggregation_field_names,
    )

    return excel.to_excel()
