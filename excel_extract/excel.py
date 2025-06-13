from collections.abc import Iterable
from typing import Generator

from django.db import models

from excel_extract.processors import Processor
from excel_extract.response import ExcelResponse


class Excel:
    """
    A class to generate Excel responses from Django model querysets.

    Attributes:
        model (models.Model): The Django model class.
        queryset (models.QuerySet or iterable): The queryset or iterable data to be processed.
        file_name (str): The name of the resulting Excel file.
        title (str): The title used in the Excel sheet.
        exclude (set[str]): Set of field names to exclude from output.
        date_format (str): Optional date formatting string.
        date_time_format (str): Optional datetime formatting string.
        bool_true (str): Representation for boolean `True`.
        bool_false (str): Representation for boolean `False`.
        fields (list): List of model fields used in export.
        fields_map (dict): Mapping of field names to verbose names.
        type_field (dict): Mapping of field names to field objects.
        verbose_name_fields (list): List of verbose names of fields used in output.
        processor (Processor): An instance of Processor to format field values.
    """

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
        """
        Initializes the Excel export helper.

        Args:
            model (models.Model): The Django model class.
            queryset (models.QuerySet): The queryset or iterable of model instances.
            file_name (str): The filename to be used in the Excel download.
            title (str): Title of the Excel document.
            exclude (list[str], optional): List of field names to exclude.
            date_format (str, optional): Format string for date fields.
            date_time_format (str, optional): Format string for datetime fields.
            bool_true (str, optional): Representation for boolean `True` values.
            bool_false (str, optional): Representation for boolean `False` values.
        """
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
        """
        Normalizes the input to ensure it's iterable.

        Args:
            queryset: A Django QuerySet or other iterable data.

        Returns:
            An iterable version of the queryset or a list containing a single item.
        """
        if isinstance(queryset, models.QuerySet):
            return queryset

        elif isinstance(queryset, Iterable) and not isinstance(
            queryset, (str, bytes)
        ):
            return queryset

        return [queryset]

    def get_fields(self):
        """
        Returns the list of verbose names of the fields used in the export.

        Returns:
            list[str]: List of verbose field names.
        """
        return [item for item in self.verbose_name_fields]

    def get_data_frame(self) -> Generator[list[str], None, None]:
        """
        Processes the queryset and yields rows of formatted values.

        Returns:
            Generator[list[str]]: A generator yielding rows of string values for Excel.
        """
        # data = []

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

            yield values

        # return data

    def to_excel(self):
        """
        Creates an ExcelResponse object from the processed data.

        Returns:
            HttpResponse: A downloadable Excel file response.
        """
        excel_response = ExcelResponse()

        data = list(self.get_data_frame())

        return excel_response.excel_response(
            file_name=self.file_name,
            title=self.title,
            data=data,
            columns=self.get_fields(),
        )
