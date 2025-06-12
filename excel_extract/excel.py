from django.db import models
from excel_extract.processors import Processor
from excel_extract.response import ExcelResponse
from collections.abc import Iterable
from typing import Generator


class Excel:

    def __init__(
        self,
        model: models.Model,
        queryset: models.QuerySet,
        file_name: str = 'file_name',
        title: str = 'title',
        exclude: list[str] = None,
        date_format: str = None,
        date_time_format: str = None,
        bool_true: str = None,
        bool_false: str = None,
    ) -> None:
        self.model = model
        self.queryset = self._get_queryset(queryset)
        self.exclude = set(exclude or [])
        self.file_name = file_name
        self.title = title
        self.date_format = date_format
        self.date_time_format = date_time_format
        self.bool_true = bool_true or 'True'
        self.bool_false = bool_false or 'False'
        self.fields = [
            field
            for field in self.model._meta.get_fields()
            if not isinstance(
                field,
                (
                    models.ManyToOneRel,
                    models.ManyToManyRel,
                    models.OneToOneRel,
                ),
            )
            and not (field.many_to_many and field.auto_created)
            and field.name not in self.exclude
        ]
        self.fields_map = {
            field.name: field.verbose_name
            for field in self.fields
            if field.name not in self.exclude
        }

        self.type_field = {field.name: field for field in self.fields}

        self.verbose_name_fields = []

        self.processor = Processor(
            date_format=self.date_format,
            date_time_format=self.date_time_format,
            bool_true=self.bool_true,
            bool_false=self.bool_false,
            exclude=self.exclude,
        )

    def _get_queryset(self, queryset):
        if isinstance(queryset, models.QuerySet):
            return queryset

        elif isinstance(queryset, Iterable) and not isinstance(
            queryset, (str, bytes)
        ):
            return queryset

        return [queryset]

    def get_fields(self):
        return [item for item in self.verbose_name_fields]

    def get_data_frame(self) -> Generator[list[str], None, None]:
        data = []

        for item in self.queryset:
            values = []

            if isinstance(item, dict):
                for field, value in item.items():
                    if field in self.fields_map:
                        field_obj = self.fields_map[field]

                        if field_obj not in self.verbose_name_fields:
                            self.verbose_name_fields.append(field_obj)

                        processor = self.processor.field_processors.get(
                            type(self.type_field.get(field))
                        )

                        if processor:
                            value = processor(
                                self.type_field.get(field), value
                            )

                        values.append(value)

                data.append(values)

            elif isinstance(item, tuple):
                pass

            else:
                for field in self.fields:

                    if field.verbose_name not in self.verbose_name_fields:
                        self.verbose_name_fields.append(field.verbose_name)

                    value = getattr(item, field.name, None)

                    processor = self.processor.field_processors.get(
                        type(field)
                    )

                    if processor:
                        value = processor(field, value)

                    values.append(value)

                data.append(values)

        return data

    def to_excel(self):
        excel_response = ExcelResponse()

        return excel_response.excel_response(
            file_name=self.file_name,
            title=self.title,
            data=self.get_data_frame(),
            columns=self.get_fields(),
        )
