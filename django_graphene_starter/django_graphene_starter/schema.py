import starter.schema
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug


class Query(
    starter.schema.Query,
    ObjectType,
):
    debug = Field(DjangoDebug, name='_debug')


class Mutation(
    starter.schema.Mutation,
    ObjectType,
):
    pass


schema = Schema(query=Query, mutation=Mutation)
