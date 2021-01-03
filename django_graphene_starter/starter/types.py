from graphene.relay import Node
from graphene_django import DjangoObjectType

from .filters import ReporterFilter
from .models import Reporter


class ReporterNode(DjangoObjectType):
    class Meta:
        model = Reporter
        interfaces = (Node,)
        filterset_class = ReporterFilter
