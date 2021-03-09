import starter.loaders as loaders
from sentry_sdk import capture_exception
from sentry_sdk.integrations.logging import ignore_logger
from starter.types import ArticleNode, ReporterNode

ignore_logger('graphql.execution.utils')


class SentryMiddleware(object):
    """
    Properly capture errors during query execution and send them to Sentry
    Then raise the error again and let Graphene handle it
    """

    def on_error(self, error):
        capture_exception(error)
        raise error

    def resolve(self, next, root, info, **args):
        return next(root, info, **args).catch(self.on_error)


class Loaders:
    def __init__(self):
        self.reporter_by_article_loader = loaders.generate_loader(ReporterNode, "id")()
        self.articles_by_reporter_loader = loaders.generate_loader_by_foreign_key(ArticleNode, 'reporter_id')()

        self.articles_by_publication_loader = loaders.generate_loader_by_many_to_many_key(ArticleNode, 'publications')()  # TODO: Need fixes. This is not working as expected


class LoaderMiddleware:
    def resolve(self, next, root, info, **args):

        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()

        return next(root, info, **args)
