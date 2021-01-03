from graphene import ID, ClientIDMutation, DateTime, Enum, Field, List, String
from graphql import GraphQLError
from graphql_relay import from_global_id

from .models import Reporter
from .types import ReporterNode


class CreateReporter(ClientIDMutation):
    reporter = Field(ReporterNode)

    class Input:
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, _, info, **input):

        first_name = input['first_name']
        last_name = input['last_name']
        email = input['email']

        reporter, created = Reporter.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        if not created:
            raise GraphQLError('Reporter already exist!')

        return CreateReporter(reporter=reporter)
