from app.views import (
    extract_excel_filter,
    extract_excel_get,
    extract_excel_values,
    extract_excel_values_list,
    index
)
from django.urls import path

urlpatterns = [
    path('index/', view=index, name='index'),
    path(
        'extract-excel-get/', view=extract_excel_get, name='extract_excel_get'
    ),
    path(
        'extract-excel-filter/',
        view=extract_excel_filter,
        name='extract_excel_filter',
    ),
    path(
        'extract-excel-values/',
        view=extract_excel_values,
        name='extract_excel_values',
    ),
    path(
        'extract-excel-values-list/',
        view=extract_excel_values_list,
        name='extract_excel_values_list',
    ),
]
