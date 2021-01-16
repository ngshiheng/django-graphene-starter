from graphene import ID, ClientIDMutation, Field, String
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from .models import Article, Publication, Reporter
from .types import ArticleNode, PublicationNode, ReporterNode


# Reporter
# ^^^^^^^^
class CreateReporter(ClientIDMutation):
    reporter = Field(ReporterNode)

    class Input:
        first_name = String(required=True)
        last_name = String(required=True)
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        first_name = input['first_name']
        last_name = input['last_name']
        username = input['username']
        email = input['email']
        password = input['password']

        reporter, created = Reporter.objects.get_or_create(
            email=email,
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
            }
        )

        reporter.set_password(password)
        reporter.save()

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


# Article
# ^^^^^^^
class CreateArticle(ClientIDMutation):
    article = Field(ArticleNode)

    class Input:
        headline = String(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        headline = input['headline']

        reporter = Reporter.objects.get(username=info.context.user.username)  # TODO: Find a better way to reference to Proxy user model

        article = Article.objects.create(headline=headline, reporter=reporter)

        return CreateArticle(article=article)


class UpdateArticle(ClientIDMutation):
    article = Field(ArticleNode)

    class Input:
        id = ID(required=True, description='ID of the Article to be updated.')
        headline = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        article = Article.objects.get(id=id)

        for field, value in input.items():
            if field != 'id':
                setattr(article, field, value)

        article.full_clean()
        article.save()

        return UpdateArticle(article=article)


class DeleteArticle(ClientIDMutation):
    article = Field(ArticleNode)

    class Input:
        id = ID(required=True, description='ID of the Article to be deleted.')

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        _, id = from_global_id(input['id'])

        article = Article.objects.get(id=id)
        article.delete()

        return DeleteArticle(article=article)
