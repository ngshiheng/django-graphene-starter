from django.contrib.auth.models import Permission
from graphene import ID, ClientIDMutation, Field, ResolveInfo, String
from graphql import GraphQLError
from graphql_jwt.decorators import login_required, permission_required, staff_member_required
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'CreateReporter':
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

        permission = Permission.objects.get(name='Can change reporter')
        reporter.user_permissions.add(permission)

        reporter.set_password(password)
        reporter.save()

        if not created:
            raise GraphQLError('Reporter already exist!')

        return CreateReporter(reporter=reporter)


class UpdateReporter(ClientIDMutation):
    """
    A reporter can only update his/her own details if he/she has `Can change reporter` permission
    """
    reporter = Field(ReporterNode)

    class Input:
        id = ID(required=True, description='ID of the Reporter to be updated.')
        first_name = String()
        last_name = String()
        email = String()

    @classmethod
    @permission_required('starter.change_reporter')
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'UpdateReporter':
        _, id = from_global_id(input['id'])

        reporter = Reporter.objects.get(id=id)

        assert info.context.user.is_staff or info.context.user == reporter, 'Permission denied. You can only update your own account.'

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
    @staff_member_required
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'DeleteReporter':
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'CreatePublication':
        title = input['title']

        publication = Publication.objects.create(title=title)

        return CreatePublication(publication=publication)


class UpdatePublication(ClientIDMutation):
    publication = Field(PublicationNode)

    class Input:
        id = ID(required=True, description='ID of the Publication to be updated.')
        title = String()

    @classmethod
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'UpdatePublication':
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'DeletePublication':
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'CreateArticle':
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'UpdateArticle':
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
    def mutate_and_get_payload(cls, root, info: ResolveInfo, **input) -> 'DeleteArticle':
        _, id = from_global_id(input['id'])

        article = Article.objects.get(id=id)
        article.delete()

        return DeleteArticle(article=article)
