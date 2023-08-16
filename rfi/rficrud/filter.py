import django_filters
from .models  import RFI


class RFIFilter(django_filters.FilterSet):
    excel_number = django_filters.CharFilter(lookup_expr='icontains')
    status = django_filters.CharFilter(lookup_expr='icontains')
    object_name = django_filters.CharFilter(field_name='object_name__object_name',
                                            lookup_expr='icontains')
    project_name = django_filters.CharFilter(field_name='project_name__name',
                                             lookup_expr='icontains')
    date_of_create_before = django_filters.DateFilter(field_name='date_of_create',
                                                      lookup_expr='lte')
    date_of_create_after = django_filters.DateFilter(field_name='date_of_create',
                                                     lookup_expr='gte')

    class Meta:
        model = RFI
        fields = ['excel_number', 'status', 'project_name', 'object_name']