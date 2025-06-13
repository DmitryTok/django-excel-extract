from app.models import Category, Report, Tags
from django.contrib import admin


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    exclude = ('report_num', 'created_at')


admin.site.register(Category)
admin.site.register(Tags)
