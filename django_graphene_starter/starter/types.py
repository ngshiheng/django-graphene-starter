from graphene import Field, Int
from graphene.relay import Connection, Node
from graphene_django import DjangoConnectionField, DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .filters import ArticleFilter, PublicationFilter, ReporterFilter
from .models import Article, Publication, Reporter


class CountableConnectionBase(Connection):
    total_count = Int(description='A total count of node in the collection.')

    class Meta:
        abstract = True

    @staticmethod
    def resolve_total_count(root, *args, **kwargs):
        if isinstance(root.iterable, list):
            return len(root.iterable)

        return root.iterable.count()


class ReporterNode(DjangoObjectType):
    articles = DjangoFilterConnectionField('starter.types.ArticleNode', description='Return a connection of Article.')
    dataloader_articles = DjangoConnectionField('starter.types.ArticleNode', description='Return Article connection which contains pagination and Article information using dataloader.')

    class Meta:
        model = Reporter
        interfaces = (Node,)
        filterset_class = ReporterFilter
        connection_class = CountableConnectionBase
        fields = ['email', 'username', 'first_name', 'last_name', 'articles']

    @staticmethod
    def resolve_articles(root: Reporter, info, **kwargs):
        return Article.objects.all()

    @staticmethod
    def resolve_dataloader_articles(root: Reporter, info, **kwargs):
        return info.context.loaders.articles_by_reporter_loader.load(root.id)


class PublicationNode(DjangoObjectType):
    dataloader_articles = DjangoConnectionField('starter.types.ArticleNode', description='Return Article connection which contains pagination and Article information using dataloader.')

    class Meta:
        model = Publication
        interfaces = (Node,)
        filterset_class = PublicationFilter
        connection_class = CountableConnectionBase

    @staticmethod
    def resolve_dataloader_articles(root: Publication, info, **kwargs):
        return info.context.loaders.articles_by_publication_loader.load(root.id)


class ArticleNode(DjangoObjectType):
    dataloader_reporter = Field('starter.types.ReporterNode', description='Get a single Reporter detail using dataloader.')

    class Meta:
        model = Article
        interfaces = (Node,)
        filterset_class = ArticleFilter
        connection_class = CountableConnectionBase

    @staticmethod
    def resolve_dataloader_reporter(root: Article, info, **kwargs):
        return info.context.loaders.reporter_by_article_loader.load(root.id)
