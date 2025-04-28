from django.contrib import admin
from app.models import Report, Category, Tags


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = ('report_num', 'created_at')


admin.site.register(Category)
admin.site.register(Tags)
