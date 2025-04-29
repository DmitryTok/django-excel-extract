import io
import pandas as pd

from django.http import HttpResponse


class ExcelResponse(HttpResponse):

    def __init__(
        self,
        data: list[list[str]],
        columns: list[str],
    ):
        self.data = data
        self.columns = columns

    def excel_response(self, file_name: str, title: str) -> HttpResponse:
        data = self.data
        columns = self.columns

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
