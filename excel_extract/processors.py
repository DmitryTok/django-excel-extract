from django.db import models
from datetime import datetime
from collections.abc import Iterable


class Processor:
    def __init__(
        self,
        date_format: str = None,
        date_time_format: str = None,
        bool_true: str = None,
        bool_false: str = None,
        choices: dict = None,
        exclude: list[str] = None,
    ):
        self.date_format = date_format
        self.date_time_format = date_time_format
        self.bool_true = bool_true
        self.bool_false = bool_false
        self.exclude = set(exclude or [])
        self.choices = choices or {}
        self.field_processors = self._generate_field_processors()

    def _generate_field_processors(self):
        return {
            models.PositiveBigIntegerField: self._process_integer,
            models.CharField: self._process_charfield,
            models.DateField: self._process_date,
            models.BooleanField: self._process_boolean,
            models.DateTimeField: self._process_datetime,
            models.ManyToManyField: self._process_many_to_many,
        }

    def _process_integer(self, field: models.Field, value: str) -> str:
        return value

    def _process_date(self, field: models.Field, value: str) -> str:
        if value == '-':
            return value

        if self.date_format:
            if isinstance(value, str):
                value = datetime.strptime(value, self.date_format)
                return value.strftime(self.date_format)
            else:
                return value.strftime(self.date_format)

    def _process_datetime(self, field: models.Field, value: str) -> str:
        if self.date_time_format:
            return value.strftime(self.date_time_format)
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def _process_boolean(self, field: models.Field, value: bool) -> str:
        if self.bool_true and self.bool_false:
            return self.bool_true if value else self.bool_false

    def _process_charfield(self, field: models.Field, value: str):
        if not field.choices:
            return value

        else:
            value = dict(field.choices).get(value, '-')
            return value

    def _process_many_to_many(
        self, field: models.Field, value: Iterable
    ) -> str:
        if not value:
            return '-'
        return ', '.join(str(item) for item in value.all())
