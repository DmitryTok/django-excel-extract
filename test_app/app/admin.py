from django.contrib import admin
from app.models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = ('report_num', 'created_at')
