from graphene import ObjectType
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import CreateReporter, DeleteReporter, UpdateReporter
from .types import ReporterNode


class Mutation(ObjectType):
    create_reporter = CreateReporter.Field(description='Create a single Reporter.')
    update_reporter = UpdateReporter.Field(description='Update a single Reporter.')
    delete_reporter = DeleteReporter.Field(description='Delete a single Reporter.')


class Query(ObjectType):
    reporter = Node.Field(ReporterNode, description='Retrieve a single Reporter node.')
    reporters = DjangoFilterConnectionField(ReporterNode, description='Return a connection of Reporter.')
