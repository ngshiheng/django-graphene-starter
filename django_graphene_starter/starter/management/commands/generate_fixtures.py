from django.core.management.base import BaseCommand
from mixer.backend.django import mixer

from ...models import Article, Publication, Reporter


class Command(BaseCommand):
    help = 'Generate fixtures for the API.'

    def add_arguments(self, parser):
        parser.add_argument('-r', '--reporters', type=int, default=10, required=False, help='How many Reporter fixtures to generate?')
        parser.add_argument('-a', '--articles', type=int, default=5, required=False, help='How many Article fixtures to generate per Reporter?')
        parser.add_argument('-p', '--publications', type=int, default=5, required=False, help='How many Publication fixtures to generate per Article?')

    def handle(self, *args, **options):
        reporters_count = options['reporters']
        articles_count = options['articles']
        publications_count = options['publications']

        for _ in range(reporters_count):
            mixer.cycle(articles_count).blend(
                Article,
                headline=mixer.faker.catch_phrase,
                publications=(mixer.cycle(publications_count).blend(Publication)),
                reporter=mixer.blend(Reporter),
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully generated fixtures: {reporters_count} Reporters | {articles_count} Articles | {publications_count} Publications.'))
