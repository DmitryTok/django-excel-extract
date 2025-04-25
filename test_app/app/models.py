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
