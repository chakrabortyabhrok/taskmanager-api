import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='iexact'
    )
    class Meta:
        model = Task
        fields = ['status', 'category']