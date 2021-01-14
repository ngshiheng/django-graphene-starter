import starter.schema
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from graphql_jwt import ObtainJSONWebToken, Verify


class Query(
    starter.schema.Query,
    ObjectType,
):
    debug = Field(DjangoDebug, name='_debug')


class Mutation(
    starter.schema.Mutation,
    ObjectType,
):
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()


schema = Schema(query=Query, mutation=Mutation)
