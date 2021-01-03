from graphene import Int
from graphene.relay import Connection, Node
from graphene_django import DjangoObjectType

from .filters import PublicationFilter, ReporterFilter
from .models import Publication, Reporter


class CountableConnectionBase(Connection):
    class Meta:
        abstract = True

    total_count = Int(description='A total count of node in the collection.')

    @staticmethod
    def resolve_total_count(root, *args, **kwargs):
        if isinstance(root.iterable, list):
            return len(root.iterable)

        return root.iterable.count()


class ReporterNode(DjangoObjectType):
    class Meta:
        model = Reporter
        interfaces = (Node,)
        filterset_class = ReporterFilter
        connection_class = CountableConnectionBase


class PublicationNode(DjangoObjectType):
    class Meta:
        model = Publication
        interfaces = (Node,)
        filterset_class = PublicationFilter
        connection_class = CountableConnectionBase
