# django-excel-extract

![PyPI download month](https://img.shields.io/pypi/dm/django-excel-extract.svg)
![PyPI version](https://badge.fury.io/py/django-excel-extract.svg)
![Python versions](https://img.shields.io/badge/python-%3E=3.9-brightgreen)
![Django Versions](https://img.shields.io/badge/django-%3E=4.2-brightgreen)

<!-- [![Coverage Status](https://coveralls.io/repos/github/farridav/django-jazzmin/badge.svg?branch=main)](https://coveralls.io/github/farridav/django-jazzmin?branch=main) -->

## Installation

```bash
pip install django-excel-extract
```

## Documentation

`django-excel-extract` helps you easily export Django model data into an Excel file (.xlsx) with minimal setup.

### Features

- Export any Django model `QuerySet` to Excel.
- Customize field output `(dates, datetimes, booleans, choices)`.
- Exclude specific fields.
- Set custom formats for dates and booleans.
- Supports `ManyToMany` fields.
- Simple integration into Django views.

---

# Usage

You must use the Excel class to generate and export an Excel file.

### Parameters

**Excel** class require parameters:

- **model** (`Model`) — Django model class to export.
- **queryset** (`QuerySet`) — Django queryset containing the data to export.
- **file_name** (`str`, optional) — Name of the generated file (default: `'file_name'`).
- **title** (`str`, optional) — Sheet title inside the Excel file (default: `'title`).
- **exclude** (`list[str]`, optional) — List of field names to exclude from export.
- **date_format** (`str`, optional) — Format string for date fields (e.g., `'%d/%m/%Y'`).
- **date_time_format** (`str`, optional) — Format string for datetime fields (e.g., `'%d/%m/%Y %H:%M'`).
- **bool_true** (`str`, optional) — Text representation for boolean `True` values (default: `'True'`).
- **bool_false** (`str`, optional) — Text representation for boolean `False` values (default: `'False'`).

### Examples

`models.py`

```python
from django.db import models
from enum import Enum
import datetime as dt
import pytz


class StatusReport(Enum):
    PENDING = 'Pending'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    FAILED = 'Failed'


class TypeReport(models.TextChoices):
    INFO = 'Information', 'Information'
    WARNING = 'Warning', 'Warning'
    ERROR = 'Error', 'Error'


class Priority(models.IntegerChoices):
    LOW = 1, 'Low'
    MEDIUM = 2, 'Medium'
    HIGH = 3, 'High'


def generate_unique_number():
    date_now = dt.datetime.now(pytz.timezone('Europe/London'))
    return int(
        f'{date_now.day}{date_now.month}{date_now.year % 1000}{date_now.hour}{date_now.minute}{date_now.microsecond}'
    )


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Category Name')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return self.name


class Tags(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tag Name')

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self) -> str:
        return self.name


class Report(models.Model):
    report_num = models.PositiveBigIntegerField(
        unique=True,
        default=generate_unique_number,
        verbose_name='Report Number',
    )
    type_report = models.CharField(
        max_length=255,
        choices=TypeReport.choices,
        verbose_name='Type of Report',
    )
    priority = models.IntegerField(
        choices=Priority.choices,
        verbose_name='Priority',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='report_category',
        verbose_name='Category',
    )
    tag = models.ManyToManyField(
        Tags,
        related_name='report_tag',
        verbose_name='Tags',
    )
    name = models.CharField(max_length=255, verbose_name='Report Name')
    status_report = models.CharField(
        max_length=255,
        choices=[(choice.name, choice.value) for choice in StatusReport],
        verbose_name='Status of Report',
    )
    description = models.TextField(verbose_name='Report Description')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date'
    )

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self) -> str:
        return f'{self.report_num} - {self.name}'
```

`views.py`

```python
from django.shortcuts import render

from app.models import Report, StatusReport, TypeReport
from excel_extract.excel import Excel


def index(request):
    return render(request, 'index.html', {})


def extract_excel(request):
    queryset = Report.objects.all()
    exclude = ['id']

    excel = Excel(
        model=Report,
        queryset=queryset,
        file_name='report',
        title='Report',
        exclude=exclude,
        date_time_format='%d/%m/%Y %H:%M',
    )

    return excel.to_excel()

```
