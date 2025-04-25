from django.urls import path
from app.views import index, extract_excel

urlpatterns = [
    path('index/', view=index, name='support'),
    path('extract-excel/', view=extract_excel, name='extract_excel'),
]
