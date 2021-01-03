from graphene import ObjectType
from graphene.relay import Node
from graphene_django.filter import DjangoFilterConnectionField

from .mutations import CreateArticle, CreatePublication, CreateReporter, DeleteArticle, DeletePublication, DeleteReporter, UpdateArticle, UpdatePublication, UpdateReporter
from .types import ArticleNode, PublicationNode, ReporterNode


class Mutation(ObjectType):
    create_reporter = CreateReporter.Field(description='Create a single Reporter.')
    update_reporter = UpdateReporter.Field(description='Update a single Reporter.')
    delete_reporter = DeleteReporter.Field(description='Delete a single Reporter.')

    create_publication = CreatePublication.Field(description='Create a single Publication.')
    update_publication = UpdatePublication.Field(description='Update a single Publication.')
    delete_publication = DeletePublication.Field(description='Delete a single Publication.')

    create_article = CreateArticle.Field(description='Create a single Article.')
    update_article = UpdateArticle.Field(description='Update a single Article.')
    delete_article = DeleteArticle.Field(description='Delete a single Article.')


class Query(ObjectType):
    reporter = Node.Field(ReporterNode, description='Retrieve a single Reporter node.')
    reporters = DjangoFilterConnectionField(ReporterNode, description='Return a connection of Reporter.')

    publication = Node.Field(PublicationNode, description='Retrieve a single Publication node.')
    publications = DjangoFilterConnectionField(PublicationNode, description='Return a connection of Publication.')

    article = Node.Field(ArticleNode, description='Retrieve a single Article node.')
    articles = DjangoFilterConnectionField(ArticleNode, description='Return a connection of Article.')
