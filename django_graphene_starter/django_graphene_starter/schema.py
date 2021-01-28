import starter.schema
from graphene import Field, ObjectType, Schema
from graphene_django.debug import DjangoDebug
from graphql_jwt import JSONWebTokenMutation, Verify
from starter.models import Reporter
from starter.types import ReporterNode


class ObtainJSONWebToken(JSONWebTokenMutation):
    reporter = Field(ReporterNode, description='Reporter node of the current user.')

    @classmethod
    def resolve(cls, root, info, **kwargs):
        reporter = Reporter.objects.get(username=info.context.user.username)  # TODO: Find a better way to reference to Proxy user model
        return cls(reporter=reporter)


class Query(
    starter.schema.Query,
    ObjectType,
):
    debug = Field(DjangoDebug, name='_debug')


class Mutation(
    starter.schema.Mutation,
    ObjectType,
):
    token_auth = ObtainJSONWebToken.Field(description='Retrieve the JWT of the user based on user credentials.')
    verify_token = Verify.Field(description='Verify a JWT token.')


schema = Schema(query=Query, mutation=Mutation)
