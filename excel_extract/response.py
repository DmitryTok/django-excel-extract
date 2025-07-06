import io

import xlsxwriter
from django.http import HttpResponse

DEBUG = True


class ExcelResponse(HttpResponse):

    def excel_response(
        self,
        file_name: str,
        title: str,
        data: list[list[str]],
        columns: list[str],
    ) -> HttpResponse:

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet(name=title)

        for col_num, col_name in enumerate(columns):
            worksheet.write(0, col_num, col_name)

        for row_num, row_data in enumerate(data, start=1):
            for col_num, cell in enumerate(row_data):
                if not isinstance(cell, (str, int, float, bool)):
                    cell = str(cell)
                worksheet.write(row_num, col_num, cell)

        workbook.close()
        output.seek(0)

        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = (
            f'attachment; filename="{file_name}.xlsx"'
        )
        return response
