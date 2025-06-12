import io
from typing import Generator

import pandas as pd

from django.http import HttpResponse

DEBUG=False


class ExcelResponse(HttpResponse):

    def __init__(
        self,
        data: Generator[list[str], None, None],
        columns: list[str],
    ):
        self.data = data
        self.columns = columns
        assert columns, "Must provide columns to generate excel file."

    def excel_response(self, file_name: str, title: str) -> HttpResponse:
        data = self.data
        columns = self.columns

        if DEBUG:
            data = list(self.data)
            print(columns)
            for i, v in enumerate(data[:5],1):
                print(i, v)

        df = pd.DataFrame(data, columns=columns)

        with io.BytesIO() as buffer:
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name=title)
            buffer.seek(0)
            response = HttpResponse(
                buffer.getvalue(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{file_name}.xlsx"'
            )
            return response
