from django.db import models


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
            models.DateField: self._process_date,
            models.BooleanField: self._process_boolean,
            models.DateTimeField: self._process_datetime,
        }

    def _process_date(
        self, field: models.Field, value: str, item: models.Model
    ) -> str:
        if self.date_format:
            return value.strftime(self.date_format)
        return value.strftime('%Y-%m-%d')

    def _process_datetime(
        self, field: models.Field, value: str, item: models.Model
    ) -> str:
        if self.date_time_format:
            return value.strftime(self.date_time_format)
        return value.strftime('%Y-%m-%d %H:%M:%S')

    def _process_boolean(
        self, field: models.Field, value: bool, item: models.Model
    ) -> str:
        if self.bool_true and self.bool_false:
            return self.bool_true if value else self.bool_false

    def _process_choices(
        self, field: models.Field, value: str, item: models.Model
    ) -> str:
        if field.name not in self.exclude:
            display_method_name = f"get_{field.name}_display"

            if hasattr(item, display_method_name):
                return getattr(item, display_method_name)()

        return value
