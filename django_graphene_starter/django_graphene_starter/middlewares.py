import starter.loaders as loaders
from starter.types import ArticleNode


class Loaders:
    def __init__(self):
        self.reporter_by_article_loader = loaders.generate_loader(ArticleNode, "id")()
        self.articles_by_reporter_loader = loaders.generate_loader_by_foreign_key(ArticleNode, 'reporter_id')()
        self.articles_by_publication_loader = loaders.generate_loader_by_many_to_many_key(ArticleNode, 'publications')()


class LoaderMiddleware:
    def resolve(self, next, root, info, **args):

        if not hasattr(info.context, 'loaders'):
            info.context.loaders = Loaders()

        return next(root, info, **args)
