from graphene import ID, ClientIDMutation, Field, String
from graphql import GraphQLError
from graphql_relay import from_global_id

from .models import Publication, Reporter
from .types import PublicationNode, ReporterNode


# Reporter
# ^^^^^^^^
class CreateReporter(ClientIDMutation):
    reporter = Field(ReporterNode)

    class Input:
        first_name = String(required=True)
        last_name = String(required=True)
        email = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

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


class UpdateReporter(ClientIDMutation):
    reporter = Field(ReporterNode)

    class Input:
        id = ID(required=True, description='ID of the Reporter to be updated.')
        first_name = String()
        last_name = String()
        email = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        reporter = Reporter.objects.get(id=id)

        for field, value in input.items():
            if field != 'id':
                setattr(reporter, field, value)

        reporter.full_clean()
        reporter.save()

        return UpdateReporter(reporter=reporter)


class DeleteReporter(ClientIDMutation):
    reporter = Field(ReporterNode)

    class Input:
        id = ID(required=True, description='ID of the Reporter to be deleted.')

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        reporter = Reporter.objects.get(id=id)
        reporter.delete()

        return DeleteReporter(reporter=reporter)


# Publication
# ^^^^^^^^^^^
class CreatePublication(ClientIDMutation):
    publication = Field(PublicationNode)

    class Input:
        title = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        title = input['title']

        publication = Publication.objects.create(title=title)

        return CreatePublication(publication=publication)


class UpdatePublication(ClientIDMutation):
    publication = Field(PublicationNode)

    class Input:
        id = ID(required=True, description='ID of the Publication to be updated.')
        title = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        publication = Publication.objects.get(id=id)

        for field, value in input.items():
            if field != 'id':
                setattr(publication, field, value)

        publication.full_clean()
        publication.save()

        return UpdatePublication(publication=publication)


class DeletePublication(ClientIDMutation):
    publication = Field(PublicationNode)

    class Input:
        id = ID(required=True, description='ID of the Publication to be deleted.')

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        publication = Publication.objects.get(id=id)
        publication.delete()

        return DeletePublication(publication=publication)
