from collections import defaultdict

from graphene.utils.subclass_with_meta import SubclassWithMeta_Meta
from promise import Promise
from promise.dataloader import DataLoader


def generate_loader_by_foreign_key(Type: SubclassWithMeta_Meta, attr: str):
    class Loader(DataLoader):
        def batch_load_fn(self, keys: list) -> Promise:
            """
            Example case of query One Reporter to Many Articles:

            Given a list of reporter id, return: { Reporter1_id: [Article1_obj, Article2_obj, Article3_obj],... }
            The idea is that for each reporter (id), return a list of Article (obj)

            >> pprint(results_by_ids)

            defaultdict(<class 'list'>,
                        {1: [<Article: Down-sized maximized firmware>,
                            <Article: Front-line mobile system engine>,
                            <Article: Implemented high-level migration>,
                            <Article: Organized incremental collaboration>,
                            <Article: Synergized well-modulated algorithm>],
                        ...
                        5: [<Article: Automated clear-thinking firmware>,
                            <Article: Intuitive radical moderator>,
                            <Article: Phased clear-thinking forecast>,
                            <Article: Proactive optimal help-desk>,
                            <Article: Proactive responsive customer loyalty>]})
            """
            results_by_ids = defaultdict(list)
            lookup = {f'{attr}__in': keys}

            # For example: Article.objects.filter(reporter_id__in=[1, 2, 3,...)
            for result in Type._meta.model.objects.filter(**lookup).iterator():
                results_by_ids[getattr(result, attr)].append(result)

            return Promise.resolve([results_by_ids.get(id, []) for id in keys])

    return Loader


def generate_loader(Type: SubclassWithMeta_Meta, attr: str):
    class Loader(DataLoader):
        def batch_load_fn(self, keys: list) -> Promise:
            """
            Example case of query One Article to One Reporter:

            Given a list of article id, return: { Article1_id: Report1_obj ,... }
            The idea is that for each article (id), return one Article (obj) associated with it

            >> pprint(results)

            {
                1056: <Reporter: Adrian Park>,
                1204: <Reporter: Jose Gentry>,
                1264: <Reporter: Nancy Coleman>,
                1380: <Reporter: Alexander Nguyen>,
                1880: <Reporter: Debbie Kirk>
            }
            """
            lookup = {f'{attr}__in': keys}

            # Article.objects.filter(id__in=[1,2,3...])
            results = {result.id: result.reporter for result in Type._meta.model.objects.filter(**lookup).iterator()}  # TODO: Remove hardcoded `result.reporter`

            return Promise.resolve([results.get(id) for id in keys])

    return Loader
