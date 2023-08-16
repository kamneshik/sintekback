from django.urls import path
from . import views

app_name = 'excelfiles'

urlpatterns = [
    path('get-rfis/', views.get_rfis, name='get_rfis'),
    path('print-page/', views.print_page, name='print_page'),
    path('create-request/', views.create_request_list, name='create_request'),
    path('from-django-to-excel/',
         views.from_django_to_excel, name='from_django_to_excel'),
    path('create_rfi/', views.create_rfi, name='create_rfi'),
    path('eftb/', views.excel_file_to_browser, name="excel_file_to_browser"),
    path('fill_rfi_numbers/', views.process_excel_file, name='fill_rfi_numbers'),
    path('success/', views.success_page, name='success'),
    path('rubka/', views.dispathcher, name='rubka'),
    path('create_daily_rfis/', views.create_daily_rfis, name='create_daily_rfis'),
    path('get_info/', views.get_information, name='get_info'),
    #path('convert_excel_to_pdf_view/', views.convert_excel_to_pdf_view, name='convert_excel_to_pdf_view'),
]

