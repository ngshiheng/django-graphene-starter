import starter.loaders as loaders
from graphene import ResolveInfo
from sentry_sdk import capture_exception
from starter.types import ArticleNode, ReporterNode


class SentryMiddleware(object):
    """
    Properly capture errors during query execution and send them to Sentry
    Then raise the error again and let Graphene handle it
    """

    def on_error(self, error):
        capture_exception(error)
        raise error

    def resolve(self, next, root, info: ResolveInfo, **args):
        """
        This will run on every single GraphQL field.

        You can think of each field in a GraphQL query as a function or method of the previous type which returns the next type.
        In fact, this is exactly how GraphQL works.
        Each field on each type is backed by a function called the resolver which is provided by the GraphQL server developer.
        When a field is executed, the corresponding resolver is called to produce the next value.

        Reference: https://graphql.org/learn/execution/
        """
        return next(root, info, **args).catch(self.on_error)


class Loaders:
    def __init__(self):
        self.reporter_by_article_loader = loaders.generate_loader(ReporterNode, "id")()
        self.articles_by_reporter_loader = loaders.generate_loader_by_foreign_key(ArticleNode, 'reporter_id')()

        self.articles_by_publication_loader = loaders.generate_loader_by_many_to_many_key(ArticleNode, 'publications')()  # FIXME: This is not working as expected


class LoaderMiddleware:
    def resolve(self, next, root, info: ResolveInfo, **args):
        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()

        return next(root, info, **args)
