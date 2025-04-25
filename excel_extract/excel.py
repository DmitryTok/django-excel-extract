import io
import pandas as pd

from django.db import models
from django.http import HttpResponse
from excel_extract.processors import Processor
from excel_extract.response import ExcelResponse


class Excel:

    def __init__(
        self,
        model: models.Model,
        queryset: models.QuerySet,
        file_name: str = 'file_name',
        title: str = 'title',
        choices: dict[str, dict[str, str]] = None,
        exclude: list[str] = None,
        date_format: str = None,
        date_time_format: str = None,
        bool_true: str = None,
        bool_false: str = None,
    ) -> None:
        self.model = model
        self.queryset = queryset
        self.exclude = set(exclude or [])
        self.file_name = file_name
        self.title = title
        self.date_format = date_format
        self.date_time_format = date_time_format
        self.bool_true = bool_true or 'True'
        self.bool_false = bool_false or 'False'
        self.choices = choices or {}
        self.fields = [
            field
            for field in self.model._meta.fields
            if field.name not in self.exclude
        ]

        self.processor = Processor(
            date_format=self.date_format,
            date_time_format=self.date_time_format,
            bool_true=self.bool_true,
            bool_false=self.bool_false,
            choices=self.choices,
            exclude=exclude,
        )

    def get_fields(self) -> list[str]:
        return [str(field.verbose_name) for field in self.fields]

    def get_data_frame(self) -> list[list[str]]:
        data = []

        for item in self.queryset:
            values = []

            for field in self.fields:
                value = getattr(item, field.name)

                if value is None:
                    value = '-'

                else:
                    processor = self.processor.field_processors.get(
                        type(field),
                        self.processor._process_choices,
                    )
                    value = processor(field, value, item)

                values.append(value)
            data.append(values)

        return data

    def to_excel(self):
        excel_response = ExcelResponse(
            data=self.get_data_frame(),
            columns=self.get_fields(),
        )
        return excel_response.excel_response(
            file_name=self.file_name, title=self.title
        )
