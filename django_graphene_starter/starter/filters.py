
from django_filters import FilterSet, OrderingFilter

from .models import Article, Publication, Reporter


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


class PublicationFilter(FilterSet):
    class Meta:
        model = Publication
        fields = ['title']

    order_by = OrderingFilter(
        fields=(
            ('title'),
        )
    )


class ArticleFilter(FilterSet):
    class Meta:
        model = Article
        fields = ['headline', 'pub_date']

    order_by = OrderingFilter(
        fields=(
            ('headline'),
            ('pub_date'),
        )
    )
