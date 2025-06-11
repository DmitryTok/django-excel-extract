import pytest
from app.models import Report


def test_excel_init(excel_empty_instance):
    assert excel_empty_instance.model == Report
    assert excel_empty_instance.queryset is not None
    assert excel_empty_instance.file_name == 'Empty_report'
    assert excel_empty_instance.title == 'Empty Report'
    assert excel_empty_instance.exclude == {'id'}
    assert excel_empty_instance.date_format == '%Y-%m-%d'
    assert excel_empty_instance.date_time_format == '%Y-%m-%d %H:%M:%S'
    assert excel_empty_instance.bool_true == 'Yes'
    assert excel_empty_instance.bool_false == 'No'


@pytest.mark.django_db
def test_excel_get_queryset(excel_empty_instance, excel_queryset):
    print(excel_empty_instance._get_queryset(excel_queryset))
