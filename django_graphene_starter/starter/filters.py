
from django_filters import FilterSet, OrderingFilter

from .models import Reporter


class ReporterFilter(FilterSet):
    class Meta:
        model = Reporter
        fields = ['email', 'first_name', 'last_name']

    order_by = OrderingFilter(
        fields=(
            ('email'),
            ('first_name'),
            ('last_name'),
        )
    )
