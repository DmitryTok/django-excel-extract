import pytest
from app.models import Report

from excel_extract import Excel

# @pytest.fixtrure
# def data():


@pytest.fixture
def excel_queryset():
    return Report.objects.all()


@pytest.fixture
def excel_empty_instance():
    return Excel(
        model=Report,
        queryset=excel_queryset,
        file_name='Empty_report',
        title='Empty Report',
        exclude=['id'],
        date_format='%Y-%m-%d',
        date_time_format='%Y-%m-%d %H:%M:%S',
        bool_true='Yes',
        bool_false='No',
    )
